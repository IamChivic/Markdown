import base64
import json
import tempfile
import os
from http.server import BaseHTTPRequestHandler
from markitdown import MarkItDown

MAX_BYTES = 4_000_000  # ~4MB safety limit for serverless request bodies


class handler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length <= 0:
                return self._send_json(400, {"error": "Empty request body"})
            if length > MAX_BYTES:
                return self._send_json(413, {"error": "File too large for this free deployment (limit ~4MB)."})

            raw = self.rfile.read(length)
            data = json.loads(raw.decode("utf-8"))

            filename = data.get("filename", "upload")
            file_b64 = data.get("file")
            if not file_b64:
                return self._send_json(400, {"error": "No file data provided"})

            file_bytes = base64.b64decode(file_b64)
            suffix = os.path.splitext(filename)[1] or ""

            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name

            try:
                md = MarkItDown(enable_plugins=False)
                result = md.convert(tmp_path)
                markdown_text = result.text_content
            finally:
                os.unlink(tmp_path)

            return self._send_json(200, {"markdown": markdown_text, "filename": filename})

        except Exception as e:
            return self._send_json(500, {"error": str(e)})
