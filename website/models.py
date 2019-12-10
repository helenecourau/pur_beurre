from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name_cat = models.CharField(max_length=150,
                                verbose_name="Nom de catégorie", unique=True)

    class Meta:
        verbose_name = "Catégorie"

    def __str__(self):

        return self.name_cat


class Product(models.Model):
    name_prod = models.CharField(max_length=255,
                                 verbose_name="Nom du produit", unique=True)
    description = models.TextField(null=True)
    grade = models.CharField(max_length=10, verbose_name="Note", null=True)
    url = models.CharField(max_length=255,
                           verbose_name="URL sur OpenFoodFact", null=True)
    url_img = models.CharField(max_length=255,
                               verbose_name="URL image", null=True)
    slug = models.SlugField(max_length=255)
    categories = models.ManyToManyField(Category, related_name='categories')
    fav = models.ManyToManyField(User, related_name='fav')

    class Meta:
        verbose_name = "Produit"

    def __str__(self):

        return self.name_prod
