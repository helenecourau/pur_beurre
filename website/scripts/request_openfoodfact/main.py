from website.scripts.request_openfoodfact import request_class as r
from website.scripts.request_openfoodfact import insert_class as i

class Main:

	def request(self, cat):
	    REQUEST = r.Request(cat)
	    REQUEST.request()
	    REQUEST.split_category()
	    INSERT = i.Insert()
	    INSERT.insert_categories(REQUEST.category)
	    INSERT.insert_product(REQUEST.foods)
	    INSERT.insert_cat_prod(REQUEST.unique_category)