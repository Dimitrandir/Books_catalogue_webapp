from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from loans.forms import LendForm
from loans.models import Loan

from .forms import BookForm, CopyForm
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
    lend_form = LendForm(initial={'date_given': timezone.now().date()})
    return render(request, 'catalog/book_detail.html', {'book': book, 'lend_form': lend_form})


def book_create(request):
    if request.method == 'POST':
        book_form = BookForm(request.POST, request.FILES)
        copy_form = CopyForm(request.POST)
        if book_form.is_valid() and copy_form.is_valid():
            book = book_form.save()
            copy = copy_form.save(commit=False)
            copy.book = book
            copy.save()
            return redirect('catalog:book_detail', pk=book.pk)
        selected_authors = Author.objects.filter(pk__in=book_form.data.getlist('authors'))
        selected_genres = Genre.objects.filter(pk__in=book_form.data.getlist('genres'))
    else:
        book_form = BookForm()
        copy_form = CopyForm()
        selected_authors = Author.objects.none()
        selected_genres = Genre.objects.none()
    context = {
        'book_form': book_form,
        'copy_form': copy_form,
        'selected_authors': selected_authors,
        'selected_genres': selected_genres,
    }
    return render(request, 'catalog/book_form.html', context)


def author_search(request):
    q = request.GET.get('q', '').strip()
    results = Author.objects.filter(name__icontains=q) if q else Author.objects.all()
    return render(request, 'catalog/_tag_search_results.html', {'results': results[:10], 'query': q})


def genre_search(request):
    q = request.GET.get('q', '').strip()
    results = Genre.objects.filter(name__icontains=q) if q else Genre.objects.all()
    return render(request, 'catalog/_tag_search_results.html', {'results': results[:10], 'query': q})
