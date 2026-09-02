from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Condition(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


def default_condition():
    return Condition.objects.get_or_create(name='Добро')[0].pk


class Book(models.Model):
    title = models.CharField(max_length=500)
    authors = models.ManyToManyField(Author, related_name='books', blank=True)
    genres = models.ManyToManyField(Genre, related_name='books', blank=True)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name='books',
    )
    year = models.IntegerField(null=True, blank=True)
    summary = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Copy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='copies')
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='copies')
    condition = models.ForeignKey(
        Condition, on_delete=models.PROTECT, related_name='copies', default=default_condition,
    )

    def __str__(self):
        return f'{self.book} ({self.location})'
