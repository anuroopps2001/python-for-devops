#### This tells you how many people are asking your AI for predictions.
```bash
sum(rate(prediction_requests_total[5m]))
```
- Why sum? If you scale your deployment to 3 replicas, sum combines them so you see the total load on your system.

#### This tracks how often your code fails (e.g., database timeouts or model crashes). (Total Errors)
```bash
sum(rate(predictions_error_total[5m]))
```
#### Error Rate % : A great engineer wants to know what percentage of requests are failing
```bash
(sum(rate(predictions_error_total[5m])) / sum(rate(prediction_requests_total[5m]))) * 100
```


#### Average Time per Prediction : `Histogram`, Prometheus automatically creates several metrics, including `_sum` and `_count`.
```bash 
rate(prediction_latency_seconds_sum[5m]) / rate(prediction_latency_seconds_count[5m])
```

#### The 95th Percentile: Average is often a "liar." To see the worst-case delay for your slowest 5% of users:
```bash
histogram_quantile(0.95, sum by (le) (rate(prediction_latency_seconds_bucket[5m])))
```

#### Query (Sell Signals per Minute):
```bash
sum(rate(sell_signal_total[1m])) * 60
```

#### 
```bash
process_resident_memory_bytes{job="stock-sell-inference-service"} / 1024 / 1024
```

# AI Inference Service Monitoring Guide

## Progress: The Four Golden Signals

Monitoring an AI pod requires four key metrics.

1. **[DONE] Latency:** Measuring the "95th person" wait time.
2. **[TODO] Traffic:** Measuring the "volume" of customers.
3. **[TODO] Errors:** Measuring the "failed" transactions.
4. **[TODO] Saturation:** Measuring the "strain" on the hardware.


## 1. Latency Percentiles (The DevOps Cheat Sheet)

When monitoring our `stock-sell-inference` pod, we use **Quantiles** to understand user experience. A higher percentile means we are looking at the "slower" end of our user base.

| Percentile (Quantile) | Who are we asking? | Why use this? |
| :--- | :--- | :--- |
| **0.50 (P50)** | The "Middle" Person | **Typical Experience.** If this number goes up, the app is fundamentally broken for everyone. |
| **0.90 (P90)** | The 90th Person | **High Standard.** Ensures that 9 out of 10 people are having a fast experience. |
| **0.95 (P95)** | **The 95th Person** | **The Industry Standard.** It ignores the 5 "weirdest" outliers but keeps pressure on the team to maintain speed. |
| **0.99 (P99)** | The 99th Person | **Mission Critical.** Used for things like payments where you want almost *zero* people to experience a delay. |



---

## 2. The "Bank Manager" Analogy

To understand our PromQL query, imagine a bank with 100 customers waiting in a single line to see the Manager (the AI Model).

### The Scenario
* **Customers:** The requests coming into our API.
* **The Manager:** Our AI Inference Pod processing the math.
* **The Wait Time:** The time it takes (Latency) to get a prediction back.

### The Query
`histogram_quantile(0.95, sum by(le) (rate(prediction_latency_seconds_bucket[5m])))`

### What does the `0.95` suggest in this query?
The **0.95** is our **Statistical Lens**. It tells the system: *"Go find the person standing at the 95th spot in line and ask them how long they waited."*

1. **Why not ask the 100th person?** The 100th person might be slow because their internet disconnected or they had a huge file. We don't want to trigger a "System Alert" for one person's bad luck.
   
2. **Why not ask the 50th person?** The 50th person (the middle) might be having a great time, while the last 10 people are waiting forever. If we only look at the middle, we are blind to the "lag" the others feel.

3. **The Result:** If the 95th person says **"I waited 1.2 seconds,"** the manager knows that **95% of the bank** finished their business in **1.2 seconds or less.**



---

## 3. How to Set the Goal (Thresholds)

We do not "set" the P95 value in the code; we **observe** it and then set a **SLA (Service Level Agreement)** goal in Grafana.

1. **Observe:** Check the P95 during a normal work hour (e.g., it stays around `0.8s`).
2. **Set Goal:** Define `1.0s` as the "Red Zone." 
3. **Protect:** If the P95 measurement moves from `0.8s` to `1.1s`, the 95th person is now unhappy, and it’s time for DevOps to investigate the CPU saturation.

---

## 4. Quick PromQL Reference

To change who you are asking in the bank, change the first number:

* **Ask the Middle Person (P50):**
  `histogram_quantile(0.50, sum by(le) (rate(prediction_latency_seconds_bucket[5m])))`

* **Ask the "Slow" Person (P95):**
  `histogram_quantile(0.95, sum by(le) (rate(prediction_latency_seconds_bucket[5m])))`



## 5. The "Three Musketeers" of Histograms

When you define a `Histogram` in your code, Prometheus automatically generates three distinct metrics. Each serves a specific purpose for the "Bank Manager."

| Metric Suffix | What it represents | Best for... |
| :--- | :--- | :--- |
| **`_bucket`** | The "Time Slots" (Pizza Boxes) | **Calculating P95/P99.** Finding out how the "slowest" users are doing. |
| **`_count`** | Total Number of Customers | **Throughput.** Seeing how many requests per second the AI is handling. |
| **`_sum`** | Total Time spent on all work | **Cost/Efficiency.** Calculating the total amount of "AI thinking time" used. |



---

### Why can't we use `_sum` and `_count` for P95?
The `_sum` and `_count` only give us the **Average**. 

**The Flaw of Averages:**
Imagine 10 customers. 9 finish in 1 second, and 1 person takes 91 seconds.
* **The Sum:** 100 seconds.
* **The Count:** 10 customers.
* **The Average:** 10 seconds.

If you only look at the **Average (10s)**, you think the bank is doing great! But the **P95 (91s)** reveals that the unlucky person is actually having a miserable experience. This is why we need the `_bucket` for P95!



---

### How to calculate the Average in Grafana
While P95 is for "User Happiness," the Average is great for "System Health." You can calculate it by dividing the total time by the total number of requests:

**Query for Average Latency:**
`rate(prediction_latency_seconds_sum[5m]) / rate(prediction_latency_seconds_count[5m])`

---

## 6. Summary Checklist for Monitoring
* Use `_bucket` + `histogram_quantile` to find **P95** (Happiness).
* Use `_sum` / `_count` to find the **Average** (Overall Efficiency).
* Use `_count` alone to see **Traffic** (Are we being hit by too many users?).

### Observation Log: Stock-Inference Pod
* **Measured P95:** 4ms - 243ms.
* **Interpretation:** The model is highly performant. The 243ms peaks represent the "worst-case" processing time under current loads.
* **Action:** Set the alerting threshold at **500ms** to allow for normal jitter without triggering false alarms.


## 7. Threshold Configuration (Grafana)

Based on our observation of the P95 hovering between 4ms and 243ms, we have configured the following thresholds:

* **Base (Green):** Healthy performance (under 300ms).
* **Warning (Yellow - 0.3s):** The app is slower than usual. Investigate for minor resource contention.
* **Critical (Red - 1.0s):** Service Level Objective (SLO) breach. 95% of users are experiencing a wait time of 1 second or more. Immediate action required.

> **Note:** Ensure the 'Unit' in Grafana is set to 'seconds' so that `0.3` is correctly displayed as `300 ms`.


## 8. Signal #2: Traffic (The Crowd)

We use a dedicated **Counter** metric to track every incoming request.

### The Query
`rate(prediction_requests_total[5m])`

### Why this is better than the Histogram count:
The `Counter` increments the moment a request arrives. The `Histogram_count` only increments when a request finishes. Using the Counter allows us to see if requests are "getting stuck" inside the system.

### Bank Analogy
This is the **Turnstile** at the front door. Even if the manager (histogram) is slow, the turnstile (separate counter for checking incoming requests) tells us exactly how many people are currently inside the building.

## 9. DevOps Philosophy: Designing for Observability

Monitoring is not about the dashboard; it is about the **underlying data model**. 

### The Three Pillars of Prometheus Knowledge:
1. **Selection:** Knowing to use a Histogram for Latency because Averages (Mean) hide the "unlucky" users.
2. **Dimensionality:** Using Labels (e.g., `method="GET"`, `status="500"`) so a single metric can answer 10 different questions.
3. **Cardinality Management:** Ensuring labels don't contain unique values (like `timestamp` or `user_id`) which would overwhelm the Prometheus database.

> "A dashboard is only as good as the labels behind it."


## 10. The Prometheus Logic Map (For DevOps)

As a DevOps Engineer, I focus on the "Data Flow" rather than just the math.

### The Flow:
1. **The Application:** Exposes raw numbers at `http://pod-ip:8000/metrics`.
2. **The Scraper:** Prometheus visits that URL every 15-30 seconds to "scrape" the numbers.
3. **The Storage:** Prometheus saves those numbers with "Labels" (metadata like `pod_name` or `status`).
4. **The Query:** We use **PromQL** to turn those raw numbers into "Rates" or "Percentiles."

### Why we use PromQL functions:
* **rate():** Because a Counter only goes up. `rate` shows us the "speed" of the increase (e.g., requests per second).
* **sum():** Because we have many pods, and we want to see the total work done by all of them combined.
* **histogram_quantile():** Because we want to find a specific "unlucky" user (like the 95th person) in a pile of data.

## 11. How to Read Raw Histogram Data

When querying `_bucket` metrics, you will see a list of labels and a value.

### The Quer
prediction_latency_seconds_bucket{service="stock-sell-inference-service"}

```bash
prediction_latency_seconds_bucket{container="inference", endpoint="http", instance="10.244.0.3:8000", job="stock-sell-inference-service", le="0.005", namespace="default", pod="stock-sell-inference-68f7ff4f87-tm4tj", service="stock-sell-inference-service"}	66
prediction_latency_seconds_bucket{container="inference", endpoint="http", instance="10.244.0.3:8000", job="stock-sell-inference-service", le="0.01", namespace="default", pod="stock-sell-inference-68f7ff4f87-tm4tj", service="stock-sell-inference-service"}	66
prediction_latency_seconds_bucket{container="inference", endpoint="http", instance="10.244.0.3:8000", job="stock-sell-inference-service", le="0.025", namespace="default", pod="stock-sell-inference-68f7ff4f87-tm4tj", service="stock-sell-inference-service"}	66
prediction_latency_seconds_bucket{container="inference", endpoint="http", instance="10.244.0.3:8000", job="stock-sell-inference-service", le="0.05", namespace="default", pod="stock-sell-inference-68f7ff4f87-tm4tj", service="stock-sell-inference-service"}	66
prediction_latency_seconds_bucket{container="inference", endpoint="http", instance="10.244.0.3:8000", job="stock-sell-inference-service", le="0.075", namespace="default", pod="stock-sell-inference-68f7ff4f87-tm4tj", service="stock-sell-inference-service"}	66
prediction_latency_seconds_bucket{container="inference", endpoint="http", instance="10.244.0.3:8000", job="stock-sell-inference-service", le="0.1", namespace="default", pod="stock-sell-inference-68f7ff4f87-tm4tj", service="stock-sell-inference-service"}	66
prediction_latency_seconds_bucket{container="inference", endpoint="http", instance="10.244.0.3:8000", job="stock-sell-inference-service", le="0.25", namespace="default", pod="stock-sell-inference-68f7ff4f87-tm4tj", service="stock-sell-inference-service"}	67
prediction_latency_seconds_bucket{container="inference", endpoint="http", instance="10.244.0.3:8000", job="stock-sell-inference-service", le="0.5", namespace="default", pod="stock-sell-inference-68f7ff4f87-tm4tj", service="stock-sell-inference-service"}	67
prediction_latency_seconds_bucket{container="inference", endpoint="http", instance="10.244.0.3:8000", job="stock-sell-inference-service", le="0.75", namespace="default", pod="stock-sell-inference-68f7ff4f87-tm4tj", service="stock-sell-inference-service"}	67
prediction_latency_seconds_bucket{container="inference", endpoint="http", instance="10.244.0.3:8000", job="stock-sell-inference-service", le="1.0", namespace="default", pod="stock-sell-inference-68f7ff4f87-tm4tj", service="stock-sell-inference-service"}	67
prediction_latency_seconds_bucket{container="inference", endpoint="http", instance="10.244.0.3:8000", job="stock-sell-inference-service", le="2.5", namespace="default", pod="stock-sell-inference-68f7ff4f87-tm4tj", service="stock-sell-inference-service"}	67
prediction_latency_seconds_bucket{container="inference", endpoint="http", instance="10.244.0.3:8000", job="stock-sell-inference-service", le="5.0", namespace="default", pod="stock-sell-inference-68f7ff4f87-tm4tj", service="stock-sell-inference-service"}	67
prediction_latency_seconds_bucket{container="inference", endpoint="http", instance="10.244.0.3:8000", job="stock-sell-inference-service", le="7.5", namespace="default", pod="stock-sell-inference-68f7ff4f87-tm4tj", service="stock-sell-inference-service"}	67
prediction_latency_seconds_bucket{container="inference", endpoint="http", instance="10.244.0.3:8000", job="stock-sell-inference-service", le="10.0", namespace="default", pod="stock-sell-inference-68f7ff4f87-tm4tj", service="stock-sell-inference-service"}	67
prediction_latency_seconds_bucket{container="inference", endpoint="http", instance="10.244.0.3:8000", job="stock-sell-inference-service", le="+Inf", namespace="default", pod="stock-sell-inference-68f7ff4f87-tm4tj", service="stock-sell-inference-service"}	67
```

### Key Label: `le` (Less than or Equal to)
* `le="0.1"`: Count of requests that finished in < 100ms.
* `le="+Inf"`: Total count of all requests (The "Infinity" bucket).

### Automatic Labels (The DevOps Context)
Prometheus enriches our Python metrics with Kubernetes metadata:
* `pod`: Exactly which replica handled the request.
* `instance`: The IP address and port.
* `namespace`: Where the app is running (e.g., `default`, `production`).

### Why this matters:
Because of these labels, we can write ONE query in Grafana and then use a "Variable" dropdown to switch between watching the whole cluster or just one specific pod.

## 12. Understanding Label Selectors (AND Logic)

Prometheus uses comma-separated labels inside `{}` to perform **AND** filtering. 

### Example Filter:
`{service="stock-sell-inference-service", namespace="production"}`
* This returns data ONLY for the inference service AND only in the production namespace.

### Common DevOps Filters:
* **Multiple Pods (Regex):** `{pod=~"stock-sell-inference-.*"}` — Selects all replicas of the inference deployment using a wildcard.
* **Excluding Errors:** `{status!="error"}` — Shows only successful requests.
* **Cross-Container:** `{container="inference"}` — Ensures you aren't accidentally looking at sidecar or logging container metrics.


## 12. Prometheus Label Selectors (The Filter Engine)

In Prometheus, filters go inside the curly braces `{}`. When you provide multiple labels, Prometheus applies **AND logic**—it only shows data that matches **every** condition provided.

### The Four Operators
| Operator | Logic | Example | Use Case |
| :--- | :--- | :--- | :--- |
| **`=`** | Equals | `{status="success"}` | Find exactly one type of result. |
| **`!=`** | Not Equals | `{namespace!="testing"}` | Exclude data you don't care about. |
| **`=~`** | Regex Match | `{pod=~"inference-.*"}` | Select all pods in a deployment. |
| **`!~`** | Regex No Match| `{pod!~".*-canary"}` | Exclude "experimental" or canary pods. |



---

### Real-World "AND" Conditions
You can stack as many conditions as you need to "zoom in" on a problem.

**1. The "Only Production AI" Filter:**
`prediction_latency_seconds_bucket{namespace="prod", container="inference"}`
* **Condition A:** Must be in the `prod` namespace.
* **Condition B:** Must be the `inference` container (ignores sidecars).

**2. The "Exclude Successful Traffic" Filter:**
`prediction_requests_total{service="stock-service", status!="success"}`
* This shows you **only** the errors and failures for that specific service.

**3. The "Wildcard" Filter (Regex):**
`sum(rate(prediction_requests_total{pod=~"stock-.*", status="error"}[1m]))`
* This finds every pod whose name starts with "stock-" and counts their errors.

---

### Troubleshooting Cheat Sheet
* **Is it global?** Remove the `pod` label and look at the `service` level.
* **Is it a specific version?** Add `{version="v2.0"}`.
* **Is it a specific node?** Add `{node="ip-10-0-1-50"}`.

> **DevOps Pro-Tip:** If your query returns "No Data," check your labels first! Prometheus is very strict—if you have a typo in a label value (like `inferene` instead of `inference`), it will return nothing even if the metric exists.

## 13. 

### Signal #3: Errors
* **Application Level (500s):** Captured by our `{status="error"}` label in Python.
* **Infrastructure Level (OOMKills/Crashes):** Captured by Kube-State-Metrics. 
* *Note:* An OOMKill will never show up in your Python `REQUEST_COUNT` because the app is dead before it can report.

### Signal #4: Saturation
* **Memory Saturation:** "How close am I to a restart?" 
  * *Calculation:* `(Used RAM / Limit) * 100`
* **CPU Saturation:** "How much is the kernel slowing me down?"
  * *Metric:* CPU Throttling.

> **DevOps Rule:** If your Error count is 0 but your users are complaining, check **Saturation**. The app might be so throttled (saturated) that it can't even produce an error!