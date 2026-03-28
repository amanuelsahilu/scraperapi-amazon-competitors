# this database is not implemented in the project and can be used for storing searched products
# basically any database can be used


from tinydb import TinyDB,Query
from datetime import datetime
import os

class Database:
    def __init__(self,db = 'data.json'):
        self.db = TinyDB(db)
        self.products = self.db.table('products')

    def insert_product(self,product_data):
        self.products.insert(product_data)

    def get_product(self,asin):
        product =Query()
        return self.products.get(product.asin == asin)
    def get_all_products(self):
        self.products.all()

    def search_product(self,search_criterion):
        product = Query()
        query = None
        for key,value in search_criterion.items():
            if not query:
                query = product[key] == value
            else:
                query &= product[key]==value
        return self.products.get(query)