import requests
from concurrent.futures import ThreadPoolExecutor

def checkSite(url: str):
    try:
        response = requests.get(url, timeout=5)
        return f"{response} is UP (Status: {response.status_code})"
    except:
        return f"{url} is DOWN"


urls = [
    "https://google.com",
    "https://github.com",
    "https://aws.amazon.com",
    "https://this-site-doesnt-exist.com"
]

with ThreadPoolExecutor(max_workers=4) as executor:  # pool of threads to execute jobs simultaneously here, 4 workers in a single pool
    result = executor.map(checkSite, urls) # checkSite (without parens) means: 
    # "Here is the reference (the blueprint) for the function. Call it later when you have a URL ready."

# The above logic-flow:
# Step A: It looks at the first item in the urls list.
# Step B: It finds an idle worker thread in the executor.
# Step C: It tells that worker: "Hey, take this specific URL and run the checkSite function with it."
# Step D: It immediately moves to the second URL and repeats the process without waiting for the first one to finish.

for r in result:
    print(r)