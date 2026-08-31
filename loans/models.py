from django.db import models

from catalog.models import Copy


class Person(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Loan(models.Model):
    copy = models.ForeignKey(Copy, on_delete=models.CASCADE, related_name='loans')
    person = models.ForeignKey(Person, on_delete=models.PROTECT, related_name='loans')
    date_given = models.DateField()
    date_returned = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-date_given']

    def __str__(self):
        status = 'върната' if self.date_returned else 'на заем'
        return f'{self.copy} → {self.person} ({status})'
