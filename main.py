import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pur_beurre.production')
django.setup()

import website.request_class as r
import website.insert_class as i

categories = ["chips", "pates-a-tartiner", "soda", "viande", "yaourt", "chocolat"]

class Main():

    def request(self, cat):
        REQUEST = r.Request(cat)
        REQUEST.request()
        REQUEST.split_category()
        INSERT = i.Insert()
        INSERT.insert_categories(REQUEST.category)
        INSERT.insert_product(REQUEST.foods)
        INSERT.insert_cat_prod(REQUEST.unique_category)

if __name__ == '__main__':
    MAIN = Main()
    for category in categories:
        MAIN.request(category)
    print('Mise à jour terminée')
