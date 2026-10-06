from flask import Flask, jsonify, render_template
from monitor import get_system_info
from network import check_websites
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/system")
def system():
    return jsonify(get_system_info())


@app.route("/api/websites")
def websites():
    return jsonify(check_websites())


@app.route("/api/health")
def health():
    return jsonify({"status": "healthy", "service": "network-monitor-dashboard"})


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
