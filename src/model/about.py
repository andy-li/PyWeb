# -*- coding: utf-8 -*-

from tornado.options import options

from pagemanage.src.db.mongodb import MongodbModel
from pagemanage.src.db import conn

_collection = "about"

class About(MongodbModel):
    def collection(self):
        return _collection

    def attributes(self):
        return ["page", "title", "content"]
     
    def findby_page(self, page):
        return self.db.find_one({'page':page})
               
def setup():
    conn.mongodb.drop_collection(_collection)
    co = getattr(conn.mongodb, _collection)
    co.ensure_index("page", unique=True)