from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    category = models.ForeignKey(
        Category, related_name='titles', on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class GenreTitle(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.SET_NULL)
    genre_id = models.ForeignKey(Genre, on_delete=models.SET_NULL)
