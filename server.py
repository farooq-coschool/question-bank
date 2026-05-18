#!/usr/bin/env python3
"""
Question Bank Generator backend.

Serves the question_bank_generator HTML, exposes POST /api/extract for PDF/image
OCR, and proxies POST /api/messages to Anthropic with the correct API key based
on the x-subject header.
"""
import io
import json
import os
import re
import traceback
import urllib.request
import urllib.error
from flask import Flask, request, jsonify, send_from_directory, Response

import fitz  # PyMuPDF
from PIL import Image
import pytesseract

ANTHROPIC_URL = 'https://api.anthropic.com/v1/messages'

_SOCIAL_KEY = os.environ.get('SOCIAL_KEY', '')
API_KEYS = {
    'Biology':     os.environ.get('BIOLOGY_KEY',     ''),
    'Physics':     os.environ.get('PHYSICS_KEY',     ''),
    'Chemistry':   os.environ.get('CHEMISTRY_KEY',   ''),
    'Mathematics': os.environ.get('MATHEMATICS_KEY', ''),
    'English':     os.environ.get('ENGLISH_KEY',     ''),
    'Commerce':    os.environ.get('COMMERCE_KEY',    ''),
    'Civics':      os.environ.get('CIVICS_KEY',      '') or _SOCIAL_KEY,
    'Geography':   os.environ.get('GEOGRAPHY_KEY',   '') or _SOCIAL_KEY,
    'History':     os.environ.get('HISTORY_KEY',     '') or _SOCIAL_KEY,
}
FORWARDED_HEADERS = {'content-type', 'anthropic-version'}

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX_HTML = 'question_bank_generator_4.html'

_tess_cmd = os.environ.get('TESSERACT_CMD')
if _tess_cmd:
    pytesseract.pytesseract.tesseract_cmd = _tess_cmd

app = Flask(__name__, static_folder=HERE, static_url_path='')


@app.after_request
def _no_cache_html(resp):
    if resp.mimetype == 'text/html':
        resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        resp.headers['Pragma'] = 'no-cache'
        resp.headers['Expires'] = '0'
    return resp


@app.route('/')
def root():
    return send_from_directory(HERE, INDEX_HTML)


@app.route('/healthz')
def health():
    return 'ok', 200


def _clean(text: str) -> str:
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def _extract_pdf(data: bytes) -> str:
    parts = []
    with fitz.open(stream=data, filetype='pdf') as doc:
        for page in doc:
            text = (page.get_text('text') or '').strip()
            if len(text) < 20:  # likely scanned -> OCR
                try:
                    pix = page.get_pixmap(dpi=200)
                    img = Image.open(io.BytesIO(pix.tobytes('png')))
                    text = pytesseract.image_to_string(img) or ''
                except Exception as e:
                    text = f'{text}\n[ocr-failed: {e}]'
            parts.append(text)
    return _clean('\n\n'.join(parts))


def _extract_image(data: bytes) -> str:
    img = Image.open(io.BytesIO(data))
    if img.mode not in ('RGB', 'L'):
        img = img.convert('RGB')
    return _clean(pytesseract.image_to_string(img) or '')


@app.route('/api/extract', methods=['POST'])
def extract():
    f = request.files.get('file')
    if not f:
        return jsonify({'error': 'no file uploaded under field "file"'}), 400
    name = (f.filename or '').lower()
    mime = (f.mimetype or '').lower()
    data = f.read()
    if not data:
        return jsonify({'error': 'empty file'}), 400
    try:
        if name.endswith('.pdf') or mime == 'application/pdf':
            text = _extract_pdf(data)
        elif mime.startswith('image/') or re.search(r'\.(png|jpg|jpeg|webp|gif|bmp|tiff)$', name):
            text = _extract_image(data)
        else:
            return jsonify({'error': f'unsupported type: {mime or name}'}), 415
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{type(e).__name__}: {e}'}), 500
    return jsonify({'text': text, 'chars': len(text)})


@app.route('/api/messages', methods=['POST', 'OPTIONS'])
def messages():
    if request.method == 'OPTIONS':
        return ('', 204, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, x-subject, anthropic-version',
        })

    subject = (request.headers.get('x-subject') or '').strip()
    api_key = API_KEYS.get(subject, '')
    if not api_key:
        return jsonify({'error': {'message': f'No API key configured for subject: "{subject}"'}}), 400

    body = request.get_data() or b''
    fwd_headers = {k: v for k, v in request.headers.items() if k.lower() in FORWARDED_HEADERS}
    fwd_headers['x-api-key'] = api_key

    req = urllib.request.Request(ANTHROPIC_URL, data=body, headers=fwd_headers, method='POST')
    try:
        with urllib.request.urlopen(req) as r:
            data = r.read()
            status = r.status
    except urllib.error.HTTPError as e:
        data = e.read()
        status = e.code
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': {'message': f'{type(e).__name__}: {e}'}}), 502

    resp = Response(data, status=status, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8000'))
    app.run(host='0.0.0.0', port=port, threaded=True)
