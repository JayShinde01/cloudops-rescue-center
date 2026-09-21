from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
app = Flask(__name__)

CORS(app)

NOTIFICATION_SERVICE_URL = os.getenv(
    "NOTIFICATION_SERVICE_URL",
    "http://localhost:5001/notify"
)
APP_ENV = os.getenv("APP_ENV", "development")
incidents = []


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/incidents", methods=["GET"])
def get_incidents():
    return jsonify(incidents)


@app.route("/incidents", methods=["POST"])
def create_incident():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    incident = {
        "id": f"INC{len(incidents) + 1:03d}",
        "title": data.get("title"),
        "severity": data.get("severity", "MEDIUM"),
        "status": "OPEN"
    }

    incidents.append(incident)

    try:
        response = requests.post(
            NOTIFICATION_SERVICE_URL,
            json=incident,
            timeout=5
        )

        print(
            "Notification service response:",
            response.status_code
        )

    except requests.RequestException as error:

        print(
            "Notification service unavailable:",
            error
        )

    return jsonify(incident), 201

@app.route("/incidents/<incident_id>", methods=["GET"])
def get_incident(incident_id):

    for incident in incidents:
        if incident["id"] == incident_id:
            return jsonify(incident)

    return jsonify({
        "error": "Incident not found"
    }), 404


@app.route("/incidents/<incident_id>", methods=["PUT"])
def update_incident(incident_id):

    data = request.get_json()

    for incident in incidents:

        if incident["id"] == incident_id:

            if "title" in data:
                incident["title"] = data["title"]

            if "severity" in data:
                incident["severity"] = data["severity"]

            if "status" in data:
                incident["status"] = data["status"]

            return jsonify(incident)

    return jsonify({
        "error": "Incident not found"
    }), 404


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )