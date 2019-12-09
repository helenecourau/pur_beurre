#URL
general = "https://fr.openfoodfacts.org/cgi/"
research = "search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0="
format_research = "&page_size=1000&json=1"

#loop
begin = 0
end = 5
space = 5

#queries

add_product = """INSERT IGNORE INTO product (name, description, url, grade)
              VALUES (%(name)s, %(description)s, %(url)s, %(grade)s)"""
add_store = """INSERT IGNORE INTO store (name) VALUES (%(name)s)"""
add_category = """INSERT IGNORE INTO category (name) VALUES (%s)"""
add_category_product = """INSERT IGNORE INTO Category_product (id_category, id_product)
                       VALUES (%(id_category)s, %(id_product)s) """
add_store_product = """INSERT IGNORE INTO Store_product (id_store, id_product)
                    VALUES (%(id_store)s, %(id_product)s)"""

select_id_name_product = """SELECT id, name FROM product """
select_id_name_store = """SELECT id, name FROM store """

select_saved_product = """SELECT Bad.name, Product.id,
                	Product.name, Product.description, Product.url, Product.grade 
                	FROM Fav_product
                	INNER JOIN Product
                	ON Product.id = Fav_Product.id_good_product
                	INNER JOIN Product as Bad
                	ON Bad.id = Fav_product.id_bad_product"""
SELECT_ID_NAME_CATEGORY = """SELECT id, name FROM category ORDER BY id """
select_product = """SELECT Product.id, Product.name AS product_name, Product.description,
                    Product.url, Product.grade, GROUP_CONCAT(Store.name SEPARATOR ', ') AS store_name 
                    FROM Product 
                    INNER JOIN Category_product 
                    ON Product.id = Category_product.id_product
                    INNER JOIN Store_product 
                    ON Product.id = Store_product.id_product 
                    INNER JOIN Store 
                    ON Store.id = Store_product.id_store                                     
                    WHERE Category_product.id_category = %(name)s
                    GROUP BY Product.name
                    ORDER BY Product.id """
add_replace_product = """INSERT IGNORE INTO Fav_product\
                      (id_bad_product, id_good_product)\
                      VALUES (%(id_bad_product)s, %(id_good_product)s)"""

#list_values
category = ["Snack"], ["Soda"], ["Yaourt"], ["Viande"], ["Sauce"]

#text

ask_init = "Voulez-vous réinitialiser la base de donnée?\
            		\nTapez 'o' pour oui et 'n' pour non :\n" 
init = "\nLa base de donnée est en train de se réinitialiser\
                		\nVeuillez patienter 30 secondes.\n"
init_ok = "\nLa base données a été réinitialisée!"
first_choice = "\nSi vous souhaitez consulter vos favoris, tapez 1.\
                	\nSi vous souhaitez accéder à notre catalogue, tapez 2 :\n"
fav = "\nVoici vos produits sauvegardés :\n"
print_fav = "\nProduit remplacé : {}\nProduit de remplacement:\
            \nNuméro d'identification : {}\nNom : {}\nURL : {}\nNote :{}\n"
category_choice = "\nSélectionnez la catégorie dont vous\
 souhaitez consulter les produits en saisissant son numéro.\n"
choose_product = "\nSélectionnez le produit que vous souhaitez remplacer\
 en saisissant son numéro ou affichez les 5 prochains produits en cliquant sur 0.\n"
chosen_product = "\nVoici le produit que vous avez choisi :\
\n\nNuméro d'identification : {}\nNom : {}\nNote : {}\n"
error_product = "\nCe n'est ni 0 ni un des numéros d'identifiants de produit,\
 recommencez svp.\n"
better_product = "Voici un produit de remplacement:\n\nNuméro d'identification :\
{}\nNom : {}\nURL : {}\nNote : {}\nDescription : {}\nOù l'acheter : {}\n"
replace = "Enregistrez le produit de remplacement en saisissant 'o' \
ou affichez un autre produit de remplacement en saisissant 'a'\n"
error = "\nCe n'est ni un '1' ni un '2'. Veuillez recommencer.\n"
end_programm = "Sélectionnez 1 pour terminer le programme et 2 pour retourner à l'accueil.\n"

