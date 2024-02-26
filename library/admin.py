from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, BookReview, Profilis


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    readonly_fields = ('id', )
    can_delete = False
    extra = 0   # išjungia papildomas tuščias eilutes įvedimui


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'isbn')
    ordering = ['title']
    inlines = [BooksInstanceInline]


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'get_author',  'status', 'reader',  'due_back')
    ordering = ['due_back']
    list_filter = ('status', 'due_back')
    search_fields = ('book__title', 'book__author__first_name', 'book__author__last_name')
    fieldsets = (
        ('Pagrindinė informacija', {'fields': ('id', 'book')}),
        ('Pasiekiamumas', {'fields': ('status', 'due_back', 'reader')}),
    )

    def get_author(self, obj):
        return obj.book.author

    get_author.short_description = 'Autorius'


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'display_books')
    ordering = ['last_name']

class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'date_created', 'reviewer', 'content')


admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(Profilis)
