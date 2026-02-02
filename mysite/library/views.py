from django.shortcuts import render
from .models import Book, Author, Genre, BookInstance
from django.views import generic

def index(request):
    context = {
        "num_books": Book.objects.count(),
        "num_instances": BookInstance.objects.count(),
        "num_instances_available": BookInstance.objects.filter(status="a").count(),
        "num_authors": Author.objects.count()
    }
    return render(request, template_name="index.html", context=context)


def authors(request):
    context = {
        'authors': Author.objects.all(),
    }
    return render(request, template_name="authors.html", context=context)


def author(request, author_id):
    context = {
        'author': Author.objects.get(pk=author_id),
    }
    return render(request, template_name="author.html", context=context)


class BookListView(generic.ListView):
    model = Book
    template_name = "books.html"
    context_object_name = "books"

