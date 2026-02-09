from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, BookReview

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'display_books']

class BookInstanceInLine(admin.TabularInline):
    model = BookInstance
    extra = 0
    can_delete = False
    readonly_fields = ['uuid']
    fields = ['uuid', 'due_back', 'reader', 'status']


class BookReviewInLine(admin.TabularInline):
    model = BookReview
    extra = 0

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'display_genre']
    inlines = [BookReviewInLine, BookInstanceInLine]

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'book', 'due_back', 'reader', 'status']
    list_filter = ['status', 'due_back', 'book']
    search_fields = ['uuid', 'book__title', 'book__author__last_name']
    list_editable = ['due_back', 'reader', 'status']

    fieldsets = [
        ('General', {'fields': ('uuid', 'book')}),
        ('Availability', {'fields': ('status', 'reader', 'due_back')}),
    ]

class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'date_created', 'reviewer', 'content']

# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(BookReview, BookReviewAdmin)