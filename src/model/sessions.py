# -*- coding: utf-8 -*-

import os
import time
from hashlib import sha1

from tornado.options import options

from pagemanage.src.db.mongodb import MongodbModel
from pagemanage.src.db import conn

_collection = "sessions"

class Session(MongodbModel):
    
        
    def collection(self):
        return _collection

    def attributes(self):
        return []
    
    def __key_gen(self):
        rand = os.urandom(16)
        now = time.time()
        return sha1("%s%s%s" %(rand, now, options.session_settings['secret_key'])).hexdigest()
    
    def get_session_key(self):
        return self.session_data['session_key']
        
    def create_new(self, handler):
        return BaseSession(self.__key_gen(), self, self.new_session_data(handler))

    def new_session_data(self, handler):
        return {'logged':0,
                'nickname':'',
                'email':'',
                'ip':handler.request.remote_ip
            }
    
    def save_session(self,session):
        self.db.save({'session_key' : session.get_session_key(), 'lastvisit': int(time.time()), 'session_data' : session})
   
    def get_session(self, session_key, handler):
        data = self.new_session_data(handler)
        if session_key:
            session_data = self.db.find_one({'session_key': session_key})
            if session_data:
                data = session_data['session_data']        
        return BaseSession(session_key, self, data)    

session_mgr = Session()
            
class BaseSession(dict):
    def __init__(self, session_key = '', mgr = None, data = {}):
        self.__session_key = session_key
        self.__mgr = mgr
        self.update(data)
        self.__change = False #小小的优化， 如果session没有改变， 就不用保存了

    def get_session_key(self):
        return self.__session_key
  
    def save(self):
        if self.__change:
            self.__mgr.save_session(self)
            self.__change = False

    # 使用session[key] 当key不存在时返回None， 防止出现异常
    def __missing__(self, key):
        return None

    def __delitem__(self, key):
        if key in self:
            del self[key]
            self.__change = True

    def __setitem__(self, key, val):
        self.__change = True
        super(BaseSession, self).__setitem__(key, val)
           
def setup():
    conn.mongodb.drop_collection(_collection)
    co = getattr(conn.mongodb, _collection)
    co.ensure_index("session_key", unique=True)
    co.ensure_index("lastvisit")

clearup = setup
