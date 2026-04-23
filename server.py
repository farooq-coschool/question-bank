#!/usr/bin/env python3
"""
Proxy server for question_bank_generator.html
- Serves the HTML/static files
- Injects the correct Anthropic API key server-side based on the x-subject header
  so keys are NEVER sent to or visible in the browser

Local usage:
    python server.py
    Open: http://localhost:8000/question_bank_generator_4.html

Cloud deployment (Render / Railway / Fly.io):
    Set environment variables for each subject key, e.g.:
        BIOLOGY_KEY=sk-ant-api03-...
        PHYSICS_KEY=sk-ant-api03-...
    The PORT env var is read automatically.
    Start command: python server.py
"""
import os
import json
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler

ANTHROPIC_URL = 'https://api.anthropic.com/v1/messages'

# ---------------------------------------------------------------------------
# API keys — set these as environment variables on your hosting platform.
# On Render: Dashboard → Environment → Add each key below.
# For local testing: set them in your shell before running server.py.
#   e.g.  set BIOLOGY_KEY=sk-ant-api03-...   (Windows)
#         export BIOLOGY_KEY=sk-ant-api03-... (Mac/Linux)
# ---------------------------------------------------------------------------
API_KEYS = {
    'Biology':     os.environ.get('BIOLOGY_KEY',     ''),
    'Physics':     os.environ.get('PHYSICS_KEY',     ''),
    'Chemistry':   os.environ.get('CHEMISTRY_KEY',   ''),
    'Mathematics': os.environ.get('MATHEMATICS_KEY', ''),
    'English':     os.environ.get('ENGLISH_KEY',     ''),
    'Civics':      os.environ.get('CIVICS_KEY',      ''),
    'Geography':   os.environ.get('GEOGRAPHY_KEY',   ''),
    'History':     os.environ.get('HISTORY_KEY',     ''),
}

# Headers from the client that are forwarded as-is (no api key here)
FORWARDED_HEADERS = {'content-type', 'anthropic-version'}


class Handler(SimpleHTTPRequestHandler):

    def do_OPTIONS(self):
        self._cors()

    def do_POST(self):
        if self.path != '/api/messages':
            self.send_response(404)
            self.end_headers()
            return

        # Identify which subject's key to use
        subject = self.headers.get('x-subject', '').strip()
        api_key = API_KEYS.get(subject, '')
        if not api_key:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self._cors()
            msg = json.dumps({'error': {'message': f'No API key configured for subject: "{subject}"'}})
            self.wfile.write(msg.encode())
            return

        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)

        # Forward safe headers, inject the api key server-side
        fwd_headers = {
            k: v for k, v in self.headers.items()
            if k.lower() in FORWARDED_HEADERS
        }
        fwd_headers['x-api-key'] = api_key  # key never touches the browser

        req = urllib.request.Request(
            ANTHROPIC_URL, data=body, headers=fwd_headers, method='POST'
        )
        try:
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
                self.send_response(resp.status)
                self.send_header('Content-Type', 'application/json')
                self._cors()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            data = e.read()
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self._cors()
            self.wfile.write(data)

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers',
                         'Content-Type, x-subject, anthropic-version')
        self.end_headers()

    def log_message(self, fmt, *args):
        print(fmt % args)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    host = '0.0.0.0'   # bind to all interfaces for cloud hosting
    server = HTTPServer((host, port), Handler)
    print(f'Serving on http://{host}:{port}')
    print(f'Open: http://localhost:{port}/question_bank_generator_4.html')
    server.serve_forever()
