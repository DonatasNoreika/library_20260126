from django.contrib import admin
from .models import Author, Genre

# Register your models here.
admin.site.register(Author)
admin.site.register(Genre)