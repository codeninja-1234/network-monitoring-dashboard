# Network Monitoring Dashboard

A containerized real-time system and network monitoring platform built with Python and Flask, with Prometheus metrics and Grafana dashboards.

## Features

- Real-time CPU, RAM and disk monitoring
- Network upload/download throughput
- Network latency monitoring
- Local IP detection
- Concurrent website health checks
- REST APIs
- `/health` service health endpoint
- Prometheus `/metrics` endpoint
- Grafana dashboard
- Docker and Docker Compose deployment
- Automated API tests
- Responsive web dashboard with live CPU graph

## Screenshot

The repository includes sample dashboard screenshots in `screenshots/`.

## Architecture

```text
System / Network
      |
      v
Python + psutil + ping3
      |
      v
Flask REST API -----> Web Dashboard
      |
      +-----> Prometheus -----> Grafana
```

## Tech Stack

Python, Flask, psutil, ping3, Requests, Prometheus, Grafana, Docker, Docker Compose, JavaScript, Chart.js, HTML/CSS, Git.

## Local setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`.

## API endpoints

- `GET /api/system` - current system and network metrics
- `GET /api/websites` - website availability and response time
- `GET /api/health` - application health
- `GET /metrics` - Prometheus metrics

## Tests

```bash
python -m unittest discover -s tests -v
```

## Docker deployment

```bash
docker compose up --build
```

Services:

- Dashboard/API: `http://localhost:5000`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

The Grafana container is provisioned with Prometheus as its default data source and a starter monitoring dashboard.

## Notes

The dashboard is intended for local/lab monitoring. Website health checks depend on outbound network access, and ICMP latency may be unavailable on some networks.
