from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from weather_service import collect_today_weather


HOST = "127.0.0.1"
PORT = 8000
BASE_DIR = Path(__file__).resolve().parent


CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".png": "image/png",
    ".ico": "image/x-icon",
}


class WeatherRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)

        if parsed.path == "/":
            self.serve_file(BASE_DIR / "index.html")
            return

        if parsed.path == "/api/weather":
            self.serve_weather(parsed.query)
            return

        requested = (BASE_DIR / unquote(parsed.path.lstrip("/"))).resolve()
        if not str(requested).startswith(str(BASE_DIR)) or not requested.is_file():
            self.send_error(404, "Not found")
            return

        self.serve_file(requested)

    def serve_weather(self, query_string: str) -> None:
        params = parse_qs(query_string)
        location = params.get("location", [""])[0].strip()
        if not location:
            self.send_json({"error": "위치를 입력해주세요."}, status=400)
            return

        try:
            self.send_json(collect_today_weather(location))
        except Exception as exc:
            self.send_json({"error": str(exc)}, status=500)

    def serve_file(self, path: Path) -> None:
        suffix = path.suffix.lower()
        content_type = CONTENT_TYPES.get(suffix, "application/octet-stream")
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, payload: dict, status: int = 200) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: object) -> None:
        print(f"{self.address_string()} - {format % args}")


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), WeatherRequestHandler)
    print(f"Weather web app running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
