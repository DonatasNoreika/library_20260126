from django.db import models


# Create your models here.
class Author(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField()
    author = models.ForeignKey(to="Author",
                               on_delete=models.SET_NULL,
                               null=True, blank=True)
    summary = models.TextField()
    isbn = models.CharField(max_length=13)
    genre = models.ManyToManyField(to="Genre")

    def __str__(self):
        return self.title