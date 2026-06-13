# TodoNoon - Python Flask Todo List

A simple Todo List web app written in **Python Flask**. It is designed to work as the single workload app for W9 GitOps + Observability + Canary.

## Features
- Python Flask server-side Todo List
- `/healthz` endpoint for Kubernetes probes
- `/metrics` endpoint for Prometheus
- `ERROR_RATE` environment variable for alert and canary auto-abort testing
- Docker-ready

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app/app.py
```

Open:

```text
http://localhost:8080
```

## Run with Docker

```bash
docker build -t todonoon-python:v1 .
docker run --rm -p 8080:8080 -e APP_VERSION=v1 -e ERROR_RATE=0 todonoon-python:v1
```

## Test injected errors

```bash
docker run --rm -p 8080:8080 -e APP_VERSION=v2-bad -e ERROR_RATE=0.5 todonoon-python:v1
```

## W9 endpoints

```text
/         Web Todo UI
/healthz  Kubernetes health check
/metrics  Prometheus metrics
/api/info JSON app info
```

## Prometheus metric

Main request counter:

```promql
flask_http_request_total
```

Example SLO query:

```promql
sum(rate(flask_http_request_total{status!~"5.."}[2m]))
/
sum(rate(flask_http_request_total[2m]))
```
