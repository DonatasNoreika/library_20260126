from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from .models import Book, Author, Genre, BookInstance
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import BookReviewForm, UserChangeForm


def index(request):
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        "num_books": Book.objects.count(),
        "num_instances": BookInstance.objects.count(),
        "num_instances_available": BookInstance.objects.filter(status="a").count(),
        "num_authors": Author.objects.count(),
        "num_visits": num_visits,
    }
    return render(request, template_name="index.html", context=context)


def authors(request):
    authors = Author.objects.all()
    paginator = Paginator(authors, per_page=3)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    context = {
        'authors': paged_authors,
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
    paginate_by = 3


class BookDetailView(FormMixin, generic.DetailView):
    model = Book
    template_name = "book.html"
    context_object_name = "book"
    form_class = BookReviewForm

    def get_success_url(self):
        return reverse('book', kwargs={"pk": self.object.pk})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.book = self.get_object()
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)


def search(request):
    query = request.GET.get('query')
    context = {
        "query": query,
        "books": Book.objects.filter(Q(title__icontains=query) |
                                     Q(author__first_name__icontains=query) |
                                     Q(author__last_name__icontains=query) |
                                     Q(summary__icontains=query)),
        "authors": Author.objects.filter(Q(first_name__icontains=query) |
                                         Q(last_name__icontains=query))
    }
    return render(request, template_name="search.html", context=context)


class MyBookInstanceListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = "my_books.html"
    context_object_name = "instances"

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user)


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy('login')


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = UserChangeForm
    template_name = "profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset = ...):
        return self.request.user

