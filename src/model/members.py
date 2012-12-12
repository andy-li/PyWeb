# -*- coding: utf-8 -*-

from pagemanage.src.db.mongodb import MongodbModel
from pagemanage.src.db import conn

_collection = "members"

class Member(MongodbModel):
    def collection(self):
        return _collection

    def attributes(self):
        return ["nickname", "email", "hash_password"]

    def findby_email(self, email):
        return self.db.find_one({"email":email})
    
    def insert_new(self, email, nickname, hash_password):
        self.db.save({'email':email, 'nickname':nickname, 'hash_password':hash_password, 'verify':[]})
    
    def update_verify(self, email=None):        
        assert email is not None, "email should be set."
        
        m = self.findby_email(email)
        assert m is not None, "no found user(_id:%s)." % _id

        v = 'email'
        verify = m['verify']
        if v not in verify:
            verify.append(v)
            self.db.update({'email':email}, {'$set':{'verify':verify}})

    def reset_passwd(self, email='', new_hash_password=''):
        self.db.update({'email':email}, {'$set':{'hash_password':new_hash_password}})
                            
                            
def setup():
    conn.mongodb.drop_collection(_collection)
    co = getattr(conn.mongodb, _collection)
    co.ensure_index("email", unique=True)