from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from catalog.models import Copy

from .forms import LendForm
from .models import Loan


def _copy_with_current_loan(copy_id):
    copy = get_object_or_404(
        Copy.objects.select_related('location', 'condition'),
        pk=copy_id,
    )
    copy.current_loan = copy.loans.filter(date_returned__isnull=True).order_by('-date_given').first()
    return copy


@login_required
@require_POST
def lend_copy(request, copy_id):
    copy = _copy_with_current_loan(copy_id)
    lend_form = LendForm(initial={'date_given': timezone.now().date()})

    if copy.current_loan is None:
        form = LendForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.copy = copy
            loan.save()
            copy.current_loan = loan
        else:
            lend_form = form

    return render(request, 'catalog/_copy_row.html', {'copy': copy, 'lend_form': lend_form})


@login_required
@require_POST
def return_loan(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id, date_returned__isnull=True)
    loan.date_returned = timezone.now().date()
    loan.save()

    copy = _copy_with_current_loan(loan.copy_id)
    lend_form = LendForm(initial={'date_given': timezone.now().date()})
    return render(request, 'catalog/_copy_row.html', {'copy': copy, 'lend_form': lend_form})
