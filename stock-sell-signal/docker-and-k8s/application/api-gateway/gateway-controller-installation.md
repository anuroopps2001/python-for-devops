### Install Envoy Gateway Controller 
```bash
kubectl apply --server-side --force-conflicts \
-f https://github.com/envoyproxy/gateway/releases/latest/download/install.yaml
```

### Verify Controller
```bash
kubectl get pods -n envoy-gateway-system
```

### Create GatewayClass

(Envoy sometimes doesn’t create it automatically)
```bash
kubectl apply -f - <<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: eg
spec:
  controllerName: gateway.envoyproxy.io/gatewayclass-controller
EOF
```

### Verify GatewayClass
```bash
kubectl get gatewayclass
```

### Create Gateway
```bash
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: envoy-gateway
  namespace: default
spec:
  gatewayClassName: eg  # This tells Envoy Gateway to "own" this
  listeners:
  - name: http
    port: 80
    protocol: HTTP
    allowedRoutes:
      namespaces:
        from: Same
```


### Create HTTPRoute
```bash
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: stock-route
  namespace: default
spec:
  parentRefs:
  - name: envoy-gateway
  rules:
  - matches:
    - path: { type: PathPrefix, value: /predict }  # Path inside the application, where request will be sent
    backendRefs:
    - name: stock-sell-inference-service
      port: 8000
```


## The Modern Traffic Stack

We have successfully moved from a "Direct-to-Service" model to a "Gateway-Managed" model.

### Traffic Flow Architecture:
1. **Client** (External curl)
2. **Envoy Gateway** (Entry point / Port 31555)   
3. **HTTPRoute** (Routing logic / Path matching)
4. **Service** (Internal load balancing)
5. **Pod** (FastAPI / AI Model execution)


```bash
curl http://192.168.49.2:31555/metrics
```

### Observability Benefits:
* **Edge Monitoring:** We catch malformed requests at the Gateway before they waste Pod CPU.
* **Service Discovery:** We can add or remove pods without ever changing our `curl` command.
* **Layered Defense:** FastAPI handles application validation, while Envoy handles network-level routing.



# Test Report: AI Stock Inference Observability
**Date:** 2026-02-05  
**Service:** `stock-sell-inference-service`  
**Infrastructure:** Kubernetes Gateway API (Envoy Gateway)

---

## 1. System Architecture & Traffic Flow
The following diagram illustrates how requests are handled and where metrics are generated at each stage:



1. **Client:** Initiates a `curl` request to the Gateway IP.
2. **Envoy Gateway:** Matches the path (`/predict` or `/health`) defined in the `HTTPRoute`.
3. **FastAPI (Python):** Validates the JSON schema via Pydantic before processing.
4. **Prometheus:** Scrapes metrics from both Envoy (Infrastructure) and the Python app (Business Logic).

---

## 2. Test Execution & Results
We performed "Negative Testing" to verify that infrastructure-level metrics catch errors that the application cannot see due to early-exit validation.

### Test Matrix
| Scenario | Command | Expected Result | Metric Recorded |
| :--- | :--- | :--- | :--- |
| **Valid Request** | `curl -X POST ... -d '{"ma_5": 1.5, ...}'` | `200 OK` | Python & Envoy (Class 2) |
| **Wrong Method** | `curl -X GET ...` | `405 Method Not Allowed` | Envoy (Class 4 / 405) |
| **Bad JSON Data** | `curl -X POST ... -d '{"ma_5": "wrong"}'` | `422 Unprocessable Entity`| Envoy (Class 4 / 422) |

### The "Silent App" Phenomenon
During **405** and **422** tests, the Python application metrics showed **no change**. 
* **Reason:** FastAPI's Pydantic validation rejects the request before it ever hits the user-defined function.
* **Solution:** We established Envoy **Upstream Metrics** as the primary source of truth for API contract health.

---

## 3. Metric Definition (Envoy Gateway)
Metrics are accessed by port-forwarding the Envoy admin port (`19001`).

### A. Aggregated Stats (Class-based)
These are used for high-level "Golden Signal" monitoring and alerting.
* **Metric:** `envoy_cluster_upstream_rq_xx`
* **Key Label:** `envoy_response_code_class`
    * `2`: Success (200, 201)
    * `4`: Client Errors (400, 404, 405, 422)
    * `5`: Server Errors (500, 503)



### B. Granular Stats (Code-based)
Used for debugging specific API integration failures.
* **Metric:** `envoy_cluster_upstream_rq_<CODE>`
    * `rq_422`: Specifically tracks schema validation failures (bad data).
    * `rq_405`: Specifically tracks incorrect HTTP verb usage.

---

## 4. Verification Procedures

### Scrapping Raw Metrics
Envoy Gateway pods are "distroless" (no `curl` inside). We use the port-forwarding method:

```bash
# 1. Establish tunnel to the Envoy pod
kubectl port-forward -n envoy-gateway-system pod/envoy-default-envoy-gateway-xxx 19001:19001

# 2. Filter for our specific application route in a separate terminal
curl -s localhost:19001/stats/prometheus | grep "stock-route"
```

#### Analyzing the Output
Successful validation is confirmed when the class="4" counter matches the number of failed curl attempts:
```bash
envoy_cluster_upstream_rq_xx{envoy_response_code_class="2", envoy_cluster_name="httproute/default/stock-route/rule/0"} 2
envoy_cluster_upstream_rq_xx{envoy_response_code_class="4", envoy_cluster_name="httproute/default/stock-route/rule/0"} 6
```

## Port Mapping & Administrative Access
```bash
ubuntu@ip-10-0-1-70:~$ kubectl get pods -n envoy-gateway-system
NAME                                                    READY   STATUS    RESTARTS   AGE
envoy-default-envoy-gateway-12b6bb46-5fc8f69796-mdkld   2/2     Running   0          77m
envoy-gateway-94db945c8-64kpv                           1/1     Running   0          86m
ubuntu@ip-10-0-1-70:~$ kubectl get svc -n envoy-gateway-system
NAME                                   TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)                                            AGE
envoy-default-envoy-gateway-12b6bb46   LoadBalancer   10.103.59.10     <pending>     80:31555/TCP                                       77m
envoy-gateway                          ClusterIP      10.101.186.113   <none>        18000/TCP,18001/TCP,18002/TCP,19001/TCP,9443/TCP   86m
ubuntu@ip-10-0-1-70:~$
```

A common point of confusion is why we can port-forward to `19001` when the LoadBalancer service only shows port `80`.

### The Separation of Concerns:
1. **Data Plane Service (`envoy-default-...`):** * **Purpose:** External user traffic.
   * **Visible Ports:** 80 (mapped to NodePort 31555).
   * **Security:** Admin ports are hidden here to prevent external attackers from seeing metrics.

2. **Control Plane Service (`envoy-gateway`):**
   * **Purpose:** Internal management and monitoring.
   * **Visible Ports:** 18000 (xDS), 19001 (Admin/Metrics).

### The Port-Forward Cheat Code:
The command `kubectl port-forward pod/<name> 19001:19001` works because it creates a direct tunnel to the **Pod's network namespace**, ignoring any Service restrictions. This allows us to inspect the "Internal State" of Envoy without exposing the metrics port to the public internet.