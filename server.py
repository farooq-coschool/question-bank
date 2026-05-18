#!/usr/bin/env python3
"""
Question Bank Generator backend.

Serves the question_bank_generator HTML and exposes POST /api/extract that
converts uploaded PDFs and images to plain text using PyMuPDF + Tesseract.

Generation calls go from the browser to Anthropic via the /api/messages
proxy in the legacy stdlib server.py; this Flask build focuses on extraction.
"""
import io
import os
import re
import traceback
from flask import Flask, request, jsonify, send_from_directory

import fitz  # PyMuPDF
from PIL import Image
import pytesseract

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX_HTML = 'question_bank_generator_4.html'

_tess_cmd = os.environ.get('TESSERACT_CMD')
if _tess_cmd:
    pytesseract.pytesseract.tesseract_cmd = _tess_cmd

app = Flask(__name__, static_folder=HERE, static_url_path='')


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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8000'))
    app.run(host='0.0.0.0', port=port, threaded=True)
