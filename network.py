import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from prometheus_client import Counter, Gauge

WEBSITES = {
    "Google": "https://www.google.com",
    "GitHub": "https://github.com",
    "Cisco": "https://www.cisco.com",
    "Stack Overflow": "https://stackoverflow.com",
}

WEBSITE_UP = Gauge(
    "website_up",
    "Website availability (1=up, 0=down)",
    ["website"],
)
WEBSITE_LATENCY = Gauge(
    "website_response_time_seconds",
    "Website response time in seconds",
    ["website"],
)
WEBSITE_CHECKS = Counter(
    "website_health_checks_total",
    "Total website health checks",
    ["website"],
)


def _check(name_url):
    name, url = name_url
    start = time.perf_counter()

    try:
        response = requests.get(
            url,
            timeout=3,
            allow_redirects=True,
            headers={"User-Agent": "NetworkMonitor/1.0"},
        )
        elapsed = round(time.perf_counter() - start, 3)
        online = response.ok
        status = "Online" if online else "Offline"
        code = response.status_code
    except requests.RequestException:
        elapsed = round(time.perf_counter() - start, 3)
        online = False
        status = "Offline"
        code = None

    WEBSITE_UP.labels(name).set(1 if online else 0)
    WEBSITE_LATENCY.labels(name).set(elapsed)
    WEBSITE_CHECKS.labels(name).inc()

    return {
        "name": name,
        "status": status,
        "status_code": code,
        "latency": elapsed,
    }


def check_websites():
    with ThreadPoolExecutor(max_workers=min(4, len(WEBSITES))) as executor:
        futures = [executor.submit(_check, item) for item in WEBSITES.items()]
        return [future.result() for future in as_completed(futures)]
