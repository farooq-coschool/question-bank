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
import time
import random
import urllib.request
import urllib.error
from flask import Flask, request, jsonify, send_from_directory, Response

import fitz  # PyMuPDF
from PIL import Image
import pytesseract

ANTHROPIC_URL = 'https://api.anthropic.com/v1/messages'

_SOCIAL_KEY = os.environ.get('SOCIAL_KEY', '') or os.environ.get('social_key', '') or os.environ.get('SOCIAL_API_KEY', '')
API_KEYS = {
    'Biology':     os.environ.get('BIOLOGY_KEY',     ''),
    'Physics':     os.environ.get('PHYSICS_KEY',     ''),
    'Chemistry':   os.environ.get('CHEMISTRY_KEY',   ''),
    'Mathematics': os.environ.get('MATHEMATICS_KEY', ''),
    'English':     os.environ.get('ENGLISH_KEY',     ''),
    'Economics':   os.environ.get('ECONOMICS_KEY',    '') or os.environ.get('ECONOMICS_API_KEY', '') or os.environ.get('COMMERCE_KEY', ''),
    'Commerce':    os.environ.get('COMMERCE_KEY',    ''),
    'Social':      _SOCIAL_KEY,
    'Civics':      os.environ.get('CIVICS_KEY',      '') or _SOCIAL_KEY,
    'Geography':   os.environ.get('GEOGRAPHY_KEY',   '') or _SOCIAL_KEY,
    'History':     os.environ.get('HISTORY_KEY',     '') or _SOCIAL_KEY,
}
FORWARDED_HEADERS = {'content-type', 'anthropic-version'}

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX_HTML = 'question_bank_generator_4.html'

CBSE_PROMPT_FILES = {
    'Biology': 'biology_cbse_prompts.js',
    'Chemistry': 'chemistry_cbse_prompts.js',
    'Mathematics': 'mathematics_cbse_prompts.js',
    'Physics': 'physics_cbse_prompts.js',
}

PROMPT_TITLE_MAP = [
    ('auto_prerequisites', 'PRE_REQUISITE', 'PRE_REQUISITE_CREATION_PROMPT'),
    ('auto_terms', 'TERMS_DEFINITIONS', 'TERMS_DEFINITIONS_CREATION_PROMPT'),
    ('auto_learning_outcomes', 'LEARNING_OUTCOMES', 'LEARNING_OUTCOMES_CREATION_PROMPT'),
    ('auto_plt_creation', 'PLT', 'PLT_CREATION_PROMPT'),
    ('auto_glossary', 'GLOSSARY', 'GLOSSARY_CREATION_PROMPT'),
    ('auto_objective_questions', 'OBJECTIVE', 'OBJECTIVE_CREATION_PROMPT'),
    ('auto_subjective_questions', 'SUBJECTIVE', 'SUBJECTIVE_CREATION_PROMPT'),
    ('auto_learning_outcomes_validation', 'LEARNING_OUTCOMES_VALIDATION', 'LO_VALIDATION_PROMPT'),
    ('auto_plt_validation', 'PLT_VALIDATION', 'PLT_VALIDATION_PROMPT'),
]

GENERATION_PROMPT_SUFFIXES = [
    'PRE_REQUISITE',
    'TERMS_DEFINITIONS',
    'LEARNING_OUTCOMES',
    'PLT',
    'GLOSSARY',
    'OBJECTIVE',
    'SUBJECTIVE',
    'REASON_ASSERTION',
]

_prompt_cache = {}

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


def _normalise_grade(value: str) -> str:
    digits = re.sub(r'\D+', '', value or '')
    return (digits or '09').zfill(2)[-2:]


def _prompt_base(subject: str, curriculum: str, grade: str) -> str:
    return f"{subject.upper().replace(' ', '_')}_{curriculum.upper()}_{_normalise_grade(grade)}"


def _load_prompt_docs(subject: str):
    if subject in _prompt_cache:
        return _prompt_cache[subject]

    filename = CBSE_PROMPT_FILES.get(subject)
    if not filename:
        raise ValueError(f'No external prompt file configured for {subject}')
    path = os.path.join(HERE, filename)
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    eq_idx = text.find('=')
    start_idx = text.find('[', eq_idx)
    end_idx = text.rfind('];')
    if eq_idx < 0 or start_idx < 0 or end_idx < start_idx:
        raise ValueError(f'Could not parse prompt docs from {filename}')

    docs = json.loads(text[start_idx:end_idx + 1])
    _prompt_cache[subject] = docs
    return docs


def _resolve_cbse_prompt_map(subject: str, grade: str):
    docs = _load_prompt_docs(subject)
    base = _prompt_base(subject, 'CBSE', grade)
    by_title = {}
    for doc in docs:
        if not doc or doc.get('isActive') is False:
            continue
        if (doc.get('subject') or '').strip() != subject:
            continue
        if (doc.get('curriculum') or '').strip().upper() != 'CBSE':
            continue
        by_title[str(doc.get('title') or '').strip()] = str(doc.get('data') or '').strip()

    prompts = {}
    for title, suffix, section_name in PROMPT_TITLE_MAP:
        body = by_title.get(title, '')
        if body:
            prompts[f'{base}_{suffix}'] = f'## {section_name}\n{body}'

    bundle_parts = [
        prompts.get(f'{base}_{suffix}', '').strip()
        for suffix in GENERATION_PROMPT_SUFFIXES
    ]
    prompts[base] = '\n\n---\n\n'.join(part for part in bundle_parts if part)
    return base, prompts


@app.route('/api/prompts/resolve', methods=['GET'])
def resolve_prompts():
    subject = (request.args.get('subject') or '').strip()
    curriculum = (request.args.get('curriculum') or 'CBSE').strip().upper()
    grade = _normalise_grade(request.args.get('grade') or '09')
    if curriculum != 'CBSE':
        return jsonify({'error': 'External prompt resolver is currently used for CBSE prompt files only.'}), 400
    if subject not in CBSE_PROMPT_FILES:
        return jsonify({'error': f'No external CBSE prompt file configured for subject: {subject}'}), 404

    try:
        prompt_key, prompts = _resolve_cbse_prompt_map(subject, grade)
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'{type(e).__name__}: {e}'}), 500

    return jsonify({
        'subject': subject,
        'curriculum': curriculum,
        'grade': grade,
        'promptKey': prompt_key,
        'prompts': prompts,
        'sections': sorted(prompts.keys()),
    })


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

    retryable_statuses = {408, 409, 425, 429, 500, 502, 503, 504, 529}
    max_attempts = int(os.environ.get('ANTHROPIC_PROXY_ATTEMPTS', '3') or '3')
    data = b''
    status = 502

    for attempt in range(1, max(1, max_attempts) + 1):
        req = urllib.request.Request(ANTHROPIC_URL, data=body, headers=fwd_headers, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                data = r.read()
                status = r.status
            break
        except urllib.error.HTTPError as e:
            data = e.read()
            status = e.code
            if status not in retryable_statuses or attempt >= max_attempts:
                break
            delay = min(20.0, (1.8 * (2 ** (attempt - 1))) + random.uniform(0.2, 1.2))
            time.sleep(delay)
        except urllib.error.URLError as e:
            if attempt >= max_attempts:
                traceback.print_exc()
                reason = getattr(e, 'reason', e)
                return jsonify({'error': {'message': f"Anthropic connection failed for {subject or 'unknown subject'} after {attempt} attempts: {reason}"}}), 502
            delay = min(20.0, (1.8 * (2 ** (attempt - 1))) + random.uniform(0.2, 1.2))
            time.sleep(delay)
        except Exception as e:
            if attempt >= max_attempts:
                traceback.print_exc()
                return jsonify({'error': {'message': f"Anthropic proxy failed for {subject or 'unknown subject'} after {attempt} attempts: {type(e).__name__}: {e}"}}), 502
            delay = min(20.0, (1.8 * (2 ** (attempt - 1))) + random.uniform(0.2, 1.2))
            time.sleep(delay)

    resp = Response(data, status=status, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8000'))
    app.run(host='0.0.0.0', port=port, threaded=True)
