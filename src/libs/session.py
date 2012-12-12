# -*- coding: utf-8 -*-

from tornado.options import options
from decorator import decorator

from pagemanage.src.db.sessions import session_mgr
from pagemanage.src.db import conn

def session():
    pass
"""
    def wrapper(func, self, *args, **kwargs):
        session_key = self.get_secure_cookie(options.session_settings['cookie_name'])

        if session_key:   
            setattr(self, "_session", session_mgr.get_session(session_key, self))               
        else:
            sess =  session_mgr.create_new(self)
            self.set_secure_cookie(options.session_settings['cookie_name'], sess.get_session_key())
            setattr(self, "_session", sess)
        
        func(self, *args, **kwargs)
        
        self._session.save()        
                    
    return decorator(wrapper)
"""