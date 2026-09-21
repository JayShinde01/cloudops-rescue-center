from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/notify", methods=["POST"])
def notify():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    incident_id = data.get("id")
    title = data.get("title")
    severity = data.get("severity")

    print("\n🚨 NEW INCIDENT")
    print(f"ID: {incident_id}")
    print(f"Title: {title}")
    print(f"Severity: {severity}")
    print("Notification processed successfully.\n")

    return jsonify({
        "message": "Notification processed successfully",
        "incidentId": incident_id
    }), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )