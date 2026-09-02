import requests

TIMEOUT = 8


def enrich(title='', author=''):
    """Търси в Open Library по заглавие+автор за резюме/година. {} ако нищо не е намерено."""
    if not title:
        return {}

    try:
        response = requests.get(
            'https://openlibrary.org/search.json',
            params={'title': title, 'author': author, 'limit': 1},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        docs = response.json().get('docs') or []
    except (requests.RequestException, ValueError):
        return {}

    if not docs:
        return {}

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
