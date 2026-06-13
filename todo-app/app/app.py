import os
import random
import time
from datetime import datetime

from flask import Flask, Response, abort, jsonify, redirect, render_template, request, url_for
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", os.getenv("VERSION", "v1"))
ERROR_RATE = float(os.getenv("ERROR_RATE", "0"))

TODOS = [
    {"id": 1, "title": "Prepare GitOps repo structure", "done": True, "created_at": "09:00"},
    {"id": 2, "title": "Expose /metrics for Prometheus", "done": False, "created_at": "09:15"},
    {"id": 3, "title": "Test canary auto-abort", "done": False, "created_at": "09:30"},
]
NEXT_ID = 4

REQUEST_COUNT = Counter(
    "flask_http_request_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "flask_http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"],
)


@app.before_request
def start_timer():
    request._start_time = time.time()


@app.after_request
def record_metrics(response):
    endpoint = request.endpoint or "unknown"
    method = request.method
    status = str(response.status_code)
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()

    if hasattr(request, "_start_time"):
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(time.time() - request._start_time)

    return response


def maybe_fail():
    """Inject random 500 errors for W9 alert/canary testing."""
    if ERROR_RATE > 0 and random.random() < ERROR_RATE:
        abort(500, description="Injected failure for canary/SLO testing")


def current_time_label():
    return datetime.now().strftime("%H:%M")


@app.route("/", methods=["GET"])
def index():
    maybe_fail()

    total = len(TODOS)
    done = len([todo for todo in TODOS if todo["done"]])
    pending = total - done

    return render_template(
        "index.html",
        todos=TODOS,
        total=total,
        done=done,
        pending=pending,
        app_version=APP_VERSION,
        error_rate=ERROR_RATE,
    )


@app.route("/todos", methods=["POST"])
def add_todo():
    maybe_fail()
    global NEXT_ID

    title = request.form.get("title", "").strip()
    if title:
        TODOS.append({
            "id": NEXT_ID,
            "title": title,
            "done": False,
            "created_at": current_time_label(),
        })
        NEXT_ID += 1

    return redirect(url_for("index"))


@app.route("/todos/<int:todo_id>/toggle", methods=["POST"])
def toggle_todo(todo_id):
    maybe_fail()

    for todo in TODOS:
        if todo["id"] == todo_id:
            todo["done"] = not todo["done"]
            break

    return redirect(url_for("index"))


@app.route("/todos/<int:todo_id>/delete", methods=["POST"])
def delete_todo(todo_id):
    maybe_fail()

    global TODOS
    TODOS = [todo for todo in TODOS if todo["id"] != todo_id]

    return redirect(url_for("index"))


@app.route("/todos/reset", methods=["POST"])
def reset_todos():
    maybe_fail()

    global TODOS, NEXT_ID
    TODOS = []
    NEXT_ID = 1

    return redirect(url_for("index"))


@app.route("/healthz", methods=["GET"])
def healthz():
    return jsonify({
        "status": "ok",
        "version": APP_VERSION,
        "error_rate": ERROR_RATE,
    })


@app.route("/api/info", methods=["GET"])
def api_info():
    maybe_fail()

    return jsonify({
        "name": "TodoNoon",
        "version": APP_VERSION,
        "error_rate": ERROR_RATE,
        "total_todos": len(TODOS),
        "completed_todos": len([todo for todo in TODOS if todo["done"]]),
    })


@app.route("/metrics", methods=["GET"])
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.errorhandler(500)
def internal_error(error):
    return render_template(
        "error.html",
        app_version=APP_VERSION,
        error_rate=ERROR_RATE,
        error=error,
    ), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
