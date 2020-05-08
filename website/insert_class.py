from .models import Category, Product
from django.utils.text import slugify


class Insert:
    '''Insert data from the OpenFoodFact API'''

    def insert_categories(self, category_list):
        for dico in category_list:
            try:
                Category.objects.get(name_cat=dico["name"])
            except Category.DoesNotExist:
                category = Category(name_cat=dico["name"])
                category.save()

    def insert_product(self, foods):
        for dico in foods:
            try:
                product = Product.objects.get(name_prod=dico["name"])
                if product.description != dico["description"]:
                    product.description = dico["description"]
                if product.grade != dico["grade"]:
                    product.grade = dico["grade"]
                if product.url != dico["url"]:
                    product.url = dico["url"]
                if product.url_img != dico["url_img"]:
                    product.url_img = dico["url_img"]
                product.save()
            except Product.DoesNotExist:
                """slug = dico["name"].replace(" ", "-").lower()"""
                product = Product(name_prod=dico["name"],
                                  description=dico["description"],
                                  grade=dico["grade"],
                                  url=dico["url"],
                                  url_img=dico["url_img"],
                                  slug=slugify(dico["name"]))
                product.save()

    def insert_cat_prod(self, unique_category):
        for dico in unique_category:
            for key, value in dico.items():
                product = Product.objects.get(name_prod=value)
                cat = Category.objects.get(name_cat=key)
                product.categories.add(cat.id)
