# -*- coding: utf-8 -*-

from pagemanage.src.db.mongodb import MongodbModel
from pagemanage.src.db import conn

_collection = "caches"

class Cache(MongodbModel):
    def collection(self):
        return _collection

    def attributes(self):
        return ["key", "value", "expire"]

    def findby_key(self, key):
        return self.db.find_one({"key":key})

def setup():
    conn.mongodb.drop_collection(_collection)
    co = getattr(conn.mongodb, _collection)
    co.ensure_index("key", unique=True)

clearup = setup