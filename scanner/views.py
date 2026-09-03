from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from catalog.models import Author, Publisher
from catalog.views import _normalize_name

from . import claude_client, open_library


def _match_or_create(model, raw_name):
    name = _normalize_name(raw_name)
    if not name:
        return None
    item, _ = model.objects.get_or_create(name__iexact=name, defaults={'name': name})
    return {'id': item.pk, 'name': item.name}


@login_required
@require_POST
def scan_cover(request):
    photo = request.FILES.get('photo')
    if not photo:
        return JsonResponse({'error': 'Няма качена снимка.'}, status=400)

    try:
        info = claude_client.extract_cover_info(photo.read())
    except claude_client.ScanError as exc:
        return JsonResponse({'error': str(exc)}, status=502)

    enrichment = open_library.enrich(
        title=info['title'],
        author=info['authors'][0] if info['authors'] else '',
    )

    authors = [_match_or_create(Author, name) for name in info['authors']]
    authors = [a for a in authors if a]
    publisher = _match_or_create(Publisher, info['publisher']) if info['publisher'] else None

    return JsonResponse({
        'title': info['title'],
        'authors': authors,
        'publisher': publisher,
        'year': enrichment.get('year'),
        'summary': enrichment.get('summary', ''),
    })
