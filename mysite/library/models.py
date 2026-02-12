from django.contrib.auth.models import User, AbstractUser
from django.db import models
import uuid
from django.utils import timezone
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CustomUser(AbstractUser):
    photo = models.ImageField(verbose_name=_('Photo'), upload_to="profile_pics", null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = Image.open(self.photo.path)
            min_side = min(img.width, img.height)
            left = (img.width - min_side) // 2
            top = (img.height - min_side) // 2
            right = left + min_side
            bottom = top + min_side
            img = img.crop((left, top, right, bottom))
            img = img.resize((300, 300), Image.LANCZOS)
            img.save(self.photo.path)


class Author(models.Model):
    first_name = models.CharField(verbose_name=_('First Name'))
    last_name = models.CharField(verbose_name=_('Last Name'))
    description = HTMLField(verbose_name=_('Description'), default="")

    def display_books(self):
        return ", ".join(book.title for book in self.books.all())

    display_books.short_description = verbose_name=_('Books')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')


class Genre(models.Model):
    name = models.CharField(verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(verbose_name=_('Title'))
    author = models.ForeignKey(to="Author",
                               verbose_name=_('Author'),
                               on_delete=models.SET_NULL,
                               null=True, blank=True,
                               related_name="books")
    summary = models.TextField(verbose_name=_('Summary'))
    isbn = models.CharField(max_length=13)
    genre = models.ManyToManyField(to="Genre", verbose_name=_('Genre'))
    cover = models.ImageField(verbose_name=_('Cover'), upload_to="covers", null=True, blank=True)

    def display_genre(self):
        return ", ".join(genre.name for genre in self.genre.all())

    display_genre.short_description = _('Genres')

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')

    def __str__(self):
        return self.title


class BookInstance(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    book = models.ForeignKey(to="Book",
                             verbose_name=_('Book'),
                             on_delete=models.CASCADE,
                             related_name="bookinstances")
    due_back = models.DateField(verbose_name=_('Due Back'), null=True, blank=True)
    reader = models.ForeignKey(to='library.CustomUser',
                               verbose_name=_('Reader'),
                               on_delete=models.SET_NULL,
                               null=True, blank=True)

    LOAN_STATUS = (
        ('d', _('Administered')),
        ('t', _('Taken')),
        ('a', _('Available')),
        ('r', _('Reserved')),
    )

    status = models.CharField(verbose_name=_('Status'), max_length=1, choices=LOAN_STATUS, default="d")

    def is_overdue(self):
        return self.due_back and timezone.now().date() > self.due_back

    is_overdue.short_description = _('Is Overdue')

    class Meta:
        verbose_name = _('Book instance')
        verbose_name_plural = _('Book instances')

    def __str__(self):
        return f"{self.book} ({self.uuid})"


class BookReview(models.Model):
    book = models.ForeignKey(to="Book",
                             verbose_name=_('Book'),
                             on_delete=models.SET_NULL,
                             null=True, blank=True,
                             related_name='reviews')
    reviewer = models.ForeignKey(to='library.CustomUser',
                                 verbose_name=_('Reviewer'),
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    date_created = models.DateTimeField(verbose_name=_('Date Created'), auto_now_add=True)
    content = models.TextField(verbose_name=_('Content'))

    class Meta:
        ordering = ["-date_created"]
        verbose_name = _('Book review')
        verbose_name_plural = _('Book reviews')

