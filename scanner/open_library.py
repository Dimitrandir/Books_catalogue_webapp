import re

import requests

TIMEOUT = 8
YEAR_RE = re.compile(r'(1[5-9]\d{2}|20\d{2})')


def enrich(isbn='', title='', author=''):
    """Търси в Open Library за резюме/година. Връща {} ако нищо не е намерено."""
    if isbn:
        data = _by_isbn(isbn)
        if data:
            return data
    if title:
        data = _by_search(title, author)
        if data:
            return data
    return {}


def _by_isbn(isbn):
    try:
        response = requests.get(
            'https://openlibrary.org/api/books',
            params={'bibkeys': f'ISBN:{isbn}', 'format': 'json', 'jscmd': 'data'},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json().get(f'ISBN:{isbn}')
    except (requests.RequestException, ValueError):
        return None

    if not payload:
        return None

    return {
        'summary': '',
        'year': _extract_year(payload.get('publish_date', '')),
    }


def _by_search(title, author):
    try:
        response = requests.get(
            'https://openlibrary.org/search.json',
            params={'title': title, 'author': author, 'limit': 1},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        docs = response.json().get('docs') or []
    except (requests.RequestException, ValueError):
        return None

    if not docs:
        return None

    doc = docs[0]
    return {
        'summary': _work_description(doc.get('key', '')),
        'year': doc.get('first_publish_year'),
    }


def _work_description(work_key):
    if not work_key:
        return ''
    try:
        response = requests.get(f'https://openlibrary.org{work_key}.json', timeout=TIMEOUT)
        response.raise_for_status()
        description = response.json().get('description', '')
    except (requests.RequestException, ValueError):
        return ''

    if isinstance(description, dict):
        description = description.get('value', '')
    return description or ''


def _extract_year(publish_date):
    match = YEAR_RE.search(publish_date or '')
    return int(match.group(1)) if match else None
