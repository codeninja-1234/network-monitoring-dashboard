import socket
import time
from threading import Lock

import psutil
from ping3 import ping
from prometheus_client import Gauge

_state_lock = Lock()
_previous = psutil.net_io_counters()
_previous_time = time.monotonic()

CPU_USAGE = Gauge("system_cpu_usage_percent", "Current CPU usage percentage")
RAM_USAGE = Gauge("system_ram_usage_percent", "Current RAM usage percentage")
DISK_USAGE = Gauge("system_disk_usage_percent", "Current disk usage percentage")
UPLOAD_SPEED = Gauge("network_upload_bytes_per_second", "Network upload speed")
DOWNLOAD_SPEED = Gauge("network_download_bytes_per_second", "Network download speed")
LATENCY = Gauge("network_latency_milliseconds", "Network latency to probe host")


def _local_ip():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except OSError:
        try:
            return socket.gethostbyname(socket.gethostname())
        except OSError:
            return "Unavailable"


def get_system_info():
    global _previous, _previous_time

    with _state_lock:
        current = psutil.net_io_counters()
        now = time.monotonic()
        elapsed = max(now - _previous_time, 0.001)

        upload_bps = max(0, (current.bytes_sent - _previous.bytes_sent) / elapsed)
        download_bps = max(0, (current.bytes_recv - _previous.bytes_recv) / elapsed)

        _previous = current
        _previous_time = now

    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    latency = None
    try:
        result = ping("8.8.8.8", timeout=1)
        if result is not None:
            latency = round(result * 1000, 2)
    except Exception:
        pass

    uptime_seconds = int(time.time() - psutil.boot_time())
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    CPU_USAGE.set(cpu)
    RAM_USAGE.set(ram)
    DISK_USAGE.set(disk)
    UPLOAD_SPEED.set(upload_bps)
    DOWNLOAD_SPEED.set(download_bps)
    if latency is not None:
        LATENCY.set(latency)

    return {
        "cpu": round(cpu, 2),
        "ram": round(ram, 2),
        "disk": round(disk, 2),
        "uptime": f"{hours}h {minutes}m {seconds}s",
        "ip": _local_ip(),
        "upload": round(upload_bps / (1024 * 1024), 2),
        "download": round(download_bps / (1024 * 1024), 2),
        "latency": latency,
    }
