from website.scripts import request_class as r
from website.scripts import insert_class as i


class Main:

    def request(self, cat):
        REQUEST = r.Request(cat)
        REQUEST.request()
        REQUEST.split_category()
        INSERT = i.Insert()
        INSERT.insert_categories(REQUEST.category)
        INSERT.insert_product(REQUEST.foods)
        INSERT.insert_cat_prod(REQUEST.unique_category)

MAIN = Main()
MAIN.request("pates-a-tartiner")
MAIN.request("soda")
MAIN.request("viande")
MAIN.request("yaourt")
MAIN.request("chocolat")