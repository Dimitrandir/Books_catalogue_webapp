import base64
import io
import os

import anthropic
from PIL import Image, UnidentifiedImageError

MODEL = 'claude-sonnet-5'
MAX_DIMENSION = 1024

TOOL_SCHEMA = {
    'name': 'extract_book_cover',
    'description': 'Данни, разчетени от снимка на корица на книга.',
    'input_schema': {
        'type': 'object',
        'properties': {
            'title': {
                'type': 'string',
                'description': 'Заглавие на книгата, ако се разчита от корицата.',
            },
            'authors': {
                'type': 'array',
                'items': {'type': 'string'},
                'description': 'Имена на авторите, ако се разчитат.',
            },
            'publisher': {
                'type': 'string',
                'description': 'Издателство, ако се разчита от корицата.',
            },
            'isbn': {
                'type': 'string',
                'description': 'ISBN номер, ако е видим на корицата (обикновено на гърба).',
            },
        },
        'required': ['title', 'authors'],
    },
}


class ScanError(Exception):
    pass


def _resize_to_jpeg(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.load()
    except UnidentifiedImageError as exc:
        raise ScanError('Неподдържан формат на снимката.') from exc

    image = image.convert('RGB')
    image.thumbnail((MAX_DIMENSION, MAX_DIMENSION))

    buffer = io.BytesIO()
    image.save(buffer, format='JPEG', quality=85)
    return buffer.getvalue()


def extract_cover_info(image_bytes):
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        raise ScanError('ANTHROPIC_API_KEY не е конфигуриран в .env.')

    jpeg_bytes = _resize_to_jpeg(image_bytes)
    image_b64 = base64.standard_b64encode(jpeg_bytes).decode('ascii')

    client = anthropic.Anthropic(api_key=api_key)
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=[TOOL_SCHEMA],
            tool_choice={'type': 'tool', 'name': 'extract_book_cover'},
            messages=[{
                'role': 'user',
                'content': [
                    {
                        'type': 'image',
                        'source': {'type': 'base64', 'media_type': 'image/jpeg', 'data': image_b64},
                    },
                    {
                        'type': 'text',
                        'text': 'Разпознай заглавие, автори, издателство и ISBN от тази корица на книга.',
                    },
                ],
            }],
        )
    except anthropic.APIError as exc:
        raise ScanError(f'Грешка при връзка с Claude API: {exc}') from exc

    tool_use = next((block for block in response.content if block.type == 'tool_use'), None)
    if tool_use is None:
        raise ScanError('Claude не разпозна данни от снимката.')

    data = tool_use.input
    return {
        'title': (data.get('title') or '').strip(),
        'authors': [name.strip() for name in (data.get('authors') or []) if name and name.strip()],
        'publisher': (data.get('publisher') or '').strip(),
        'isbn': (data.get('isbn') or '').strip(),
    }
