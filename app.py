from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from weather_service import collect_today_weather


BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    static_folder=str(BASE_DIR / "static"),
    static_url_path="/static",
)


@app.get("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/api/weather")
def weather():
    location = request.args.get("location", "").strip()
    if not location:
        return jsonify({"error": "Location is required."}), 400

    try:
        return jsonify(collect_today_weather(location))
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.get("/favicon.ico")
def favicon():
    return "", 204


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
