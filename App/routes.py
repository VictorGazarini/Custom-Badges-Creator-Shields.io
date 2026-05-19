from urllib.parse import quote, urlencode

from flask import jsonify, render_template, request

from . import app


@app.route('/')
def index():
    return render_template('index.html')


def _clean_text(value, max_len=64):
    if value is None:
        return ''
    return str(value).strip()[:max_len]


def _build_badge_url(payload):
    message = _clean_text(payload.get('message'), 80)
    if not message:
        raise ValueError("'message' is required")

    label = _clean_text(payload.get('label'), 64)
    color = _clean_text(payload.get('color'), 40) or 'brightgreen'

    if label:
        badge_content = f"{label}-{message}-{color}"
    else:
        badge_content = f"{message}-{color}"

    encoded_badge = quote(badge_content, safe='')
    base_url = f"https://img.shields.io/badge/{encoded_badge}"

    params = {}

    style = _clean_text(payload.get('style'), 40)
    if style:
        params['style'] = style

    label_color = _clean_text(payload.get('labelColor'), 20)
    if label_color and label:
        params['labelColor'] = label_color

    logo_color = _clean_text(payload.get('logoColor'), 20)
    if logo_color:
        params['logoColor'] = logo_color

    logo_size = _clean_text(payload.get('logoSize'), 10)
    if logo_size:
        params['logoSize'] = logo_size

    logo = _clean_text(payload.get('logo'), 4000)
    if logo:
        params['logo'] = logo

    query = urlencode(params, doseq=False)
    return f"{base_url}?{query}" if query else base_url


@app.get('/api/healthz')
def healthz():
    return jsonify({'status': 'ok'}), 200


@app.post('/api/generate')
def generate_badge():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({'error': 'invalid_json', 'details': 'Send a JSON object body.'}), 400

    try:
        badge_url = _build_badge_url(payload)
    except ValueError as exc:
        return jsonify({'error': 'validation_error', 'details': str(exc)}), 400

    return jsonify({'url': badge_url}), 200
