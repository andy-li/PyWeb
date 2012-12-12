# -*- coding: utf-8 -*-

from pagemanage.src.db.mongodb import MongodbModel
from pagemanage.src.db import conn

_collection = "products"

class Product(MongodbModel):
    def collection(self):
        return _collection

    def attributes(self):
        return [
                "code", "name", "url",
                "price", "context", "status",
                "images"
            ]

    def findby_code(self, code):
        return self.db.find_one({"code":code})      

    def get_list(self, **kwargs):
        page = kwargs.get('page', 1)
        pagesize = kwargs.get('pagesize', 20)
                
        skip = (page-1) * pagesize
        
        return self.db.find().skip(skip).limit(pagesize)
    
    def deleteby_code(self, code):
        self.db.remove({'code':code})        

    def updateby_code(self, code):
        self.db.update({'code':code}, {'$set':self.record()})
                        
def setup():
    conn.mongodb.drop_collection(_collection)
    co = getattr(conn.mongodb, _collection)
    co.ensure_index("code", unique=True)