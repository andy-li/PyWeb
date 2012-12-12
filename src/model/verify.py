# -*- coding: utf-8 -*-

import time
import hashlib

from tornado.options import options

from pagemanage.src.db.mongodb import MongodbModel
from pagemanage.src.db import conn
from pagemanage.src.libs.utils import hash_password


_collection = "verify"

class Verify(MongodbModel):
            
    def collection(self):
        return _collection

    def attributes(self):
        return ["code", "type", "content", "exptime"]
    
    def hash_code(self, key):
        code = hashlib.md5()
        code.update(str(key))
        code.update(str(time.time()))
        code = code.hexdigest()
        
        verify_code = hash_password(code)
        return verify_code     
    
    def create_new(self, code, type, content):
        self.code = code
        self.type = type
        self.content =content
        self.exptime = int(time.time()) + 86400 * 3 #3 days
        self.insert()
    
    def findby_code(self, code):
        return self.db.find_one({'code':code})
               
def setup():
    conn.mongodb.drop_collection(_collection)
    co = getattr(conn.mongodb, _collection)
    co.ensure_index("code", unique=True)