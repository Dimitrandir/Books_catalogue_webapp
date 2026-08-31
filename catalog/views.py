from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from loans.models import Loan

from .models import Author, Book, Copy, Genre, Location, Publisher


def _available_copies():
    open_loans = Loan.objects.filter(date_returned__isnull=True).values('copy_id')
    return Copy.objects.exclude(id__in=open_loans)


def _on_loan_copies():
    open_loans = Loan.objects.filter(date_returned__isnull=True).values('copy_id')
    return Copy.objects.filter(id__in=open_loans)


def book_list(request):
    query = request.GET.get('q', '').strip()
    genre_id = request.GET.get('genre', '')
    author_id = request.GET.get('author', '')
    publisher_id = request.GET.get('publisher', '')
    location_id = request.GET.get('location', '')
    availability = request.GET.get('availability', '')

    books = Book.objects.select_related('publisher').prefetch_related('authors', 'genres')

    if query:
        vector = SearchVector('title', 'summary', config='simple')
        search_query = SearchQuery(query, config='simple')
        books = books.annotate(rank=SearchRank(vector, search_query)).filter(
            Q(rank__gt=0) | Q(authors__name__icontains=query)
        ).order_by('-rank', 'title')
    else:
        books = books.order_by('title')

    if genre_id:
        books = books.filter(genres__id=genre_id)
    if author_id:
        books = books.filter(authors__id=author_id)
    if publisher_id:
        books = books.filter(publisher_id=publisher_id)
    if location_id:
        books = books.filter(copies__location_id=location_id)
    if availability == 'available':
        books = books.filter(copies__in=_available_copies())
    elif availability == 'on_loan':
        books = books.filter(copies__in=_on_loan_copies())

    books = books.distinct()

    paginator = Paginator(books, 24)
    page_obj = paginator.get_page(request.GET.get('page'))

    querystring = request.GET.copy()
    querystring.pop('page', None)

    context = {
        'page_obj': page_obj,
        'query': query,
        'querystring': querystring.urlencode(),
        'genres': Genre.objects.all(),
        'authors': Author.objects.all(),
        'publishers': Publisher.objects.all(),
        'locations': Location.objects.all(),
        'selected': {
            'genre': genre_id,
            'author': author_id,
            'publisher': publisher_id,
            'location': location_id,
            'availability': availability,
        },
    }
    template = 'catalog/_book_results.html' if request.htmx else 'catalog/book_list.html'
    return render(request, template, context)


def book_detail(request, pk):
    book = get_object_or_404(
        Book.objects.select_related('publisher').prefetch_related(
            'authors', 'genres', 'copies__location', 'copies__condition', 'copies__loans__person',
        ),
        pk=pk,
    )
    for copy in book.copies.all():
        copy.current_loan = next(
            (loan for loan in copy.loans.all() if loan.date_returned is None), None
        )
    return render(request, 'catalog/book_detail.html', {'book': book})
