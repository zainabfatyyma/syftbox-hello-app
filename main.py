import json
import os
import sys
from html import escape
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs


def hello(name: str) -> str:
    return f"Hello {name}, SyftBox is working!"


def _render_page(result_text: str = "") -> bytes:
    safe_result = escape(result_text)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SyftBox Hello App</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 2rem;
      max-width: 720px;
    }}
    input, button {{
      font-size: 1rem;
      padding: 0.5rem;
      margin-right: 0.25rem;
    }}
    .result {{
      margin-top: 1rem;
      padding: 0.75rem;
      background: #f2f6ff;
      border-left: 4px solid #4066ff;
    }}
  </style>
</head>
<body>
  <h1>SyftBox Hello App</h1>
  <p>Enter text below and submit to get a dynamic response.</p>
  <form method="post" action="/">
    <input
      type="text"
      name="name"
      placeholder="Type your name"
      required
    />
    <button type="submit">Submit</button>
  </form>
  {"<div class='result'><strong>Result:</strong> " + safe_result + "</div>" if safe_result else ""}
</body>
</html>
"""
    return html.encode("utf-8")


class HelloHandler(BaseHTTPRequestHandler):
    def _write_html(self, html_bytes: bytes, status: HTTPStatus = HTTPStatus.OK) -> None:
        self.send_response(status.value)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html_bytes)))
        self.end_headers()
        self.wfile.write(html_bytes)

    def _write_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if self.path == "/":
            self._write_html(_render_page())
            return

        if self.path == "/healthz":
            self._write_json({"status": "ok"})
            return

        self._write_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)

        if self.path == "/":
            form = parse_qs(raw_body.decode("utf-8"))
            name = form.get("name", ["World"])[0].strip() or "World"
            result = hello(name)
            self._write_html(_render_page(result))
            return

        if self.path == "/api/hello":
            try:
                payload = json.loads(raw_body.decode("utf-8") or "{}")
            except json.JSONDecodeError:
                self._write_json({"error": "Invalid JSON body"}, status=HTTPStatus.BAD_REQUEST)
                return

            name = str(payload.get("name", "World")).strip() or "World"
            self._write_json({"result": hello(name)})
            return

        self._write_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)

    def log_message(self, fmt: str, *args) -> None:
        # Keep logs concise for SyftBox app logs.
        print(f"[http] {fmt % args}")


def run_web_server() -> None:
    port = int(os.environ.get("SYFTBOX_ASSIGNED_PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), HelloHandler)
    print(f"SyftBox Hello App web interface listening on port {port}")
    server.serve_forever()


def run_stdin_mode() -> None:
    raw_input = sys.stdin.read().strip()
    data = json.loads(raw_input) if raw_input else {}
    name = str(data.get("name", "World")).strip() or "World"
    print(json.dumps({"result": hello(name)}))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        run_web_server()
    else:
        run_stdin_mode()