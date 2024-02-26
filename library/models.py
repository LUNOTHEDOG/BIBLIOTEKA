from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import date
from PIL import Image

from tinymce.models import HTMLField


class Genre(models.Model):
    name = models.CharField('Pavadinimas', max_length=200, help_text='Prašome įvesti knygos žanrą')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Žanras'
        verbose_name_plural = 'Žanrai'


class Book(models.Model):
    title = models.CharField('Pavadinimas', max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, related_name='books', verbose_name='Autorius')
    summary = models.TextField('Aprašymas', max_length=1000, help_text='Knygos aprašymas')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Simbolių <a href="https://www.isbn-international.org/content/what-isbn">ISBN kodas</a>')
    genre = models.ManyToManyField(Genre, help_text='Pasirinkite žanrą', verbose_name='Žanras')
    cover = models.ImageField('Viršelis', upload_to='covers', null=True)

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Žanras'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Knyga'
        verbose_name_plural = 'Knygos'


class BookInstance(models.Model):
    id = models.UUIDField('ID', primary_key=True, default=uuid.uuid4, help_text='Unikalus ID knygos kopijai')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, verbose_name='Knyga')
    due_back = models.DateField('Bus prieinama', null=True, blank=True)
    reader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('s', 'Šiuo metu skaitoma'),
        ('p', 'Prienama'),
        ('r', 'Rezervuota'),
    )

    status = models.CharField('Knygos statusas', max_length=1, choices=LOAN_STATUS, blank=True, default='a', help_text='Statusas')

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']
        verbose_name = 'Knygos kopija'
        verbose_name_plural = 'Knygų kopijos'

    def __str__(self):
        return f'{self.id} ({self.book.author} - {self.book.title})'


class Author(models.Model):
    first_name = models.CharField('Vardas', max_length=100)
    last_name = models.CharField('Pavardė', max_length=100)
    description = HTMLField()


    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = 'Autorius'
        verbose_name_plural = 'Autoriai'

    def display_books(self):
        return ', '.join(book.title for book in self.books.all()[:3])

    display_books.short_description = 'Knygos'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class BookReview(models.Model):
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Atsiliepimas', max_length=2000)

    class Meta:
        verbose_name = "Atsiliepimas"
        verbose_name_plural = 'Atsiliepimai'
        ordering = ['-date_created']


class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    class Meta:
        verbose_name = "Profilis"
        verbose_name_plural = 'Profiliai'

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)
