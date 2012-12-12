# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime, timedelta
from decorator import decorator
from tornado.escape import utf8
from tornado.options import options

from pagemanage.src.libs.handler import BaseHandler
from pagemanage.src.db import conn
from pagemanage.src.model.caches import Cache

__all__ = ("cache", "page", "key_gen", "remove")

def cache(expire=7200, key='', anonymous=False):
    
    def wrapper(func, self, *args, **kwargs):
        now = datetime.now()
        if key:
            c = key
        else:
            c = self.__class__.__name__ + func.__name__
            
        k, handler = key_gen(self, c, anonymous, *args, **kwargs)
        
        value = Cache().findby_key(k)
        
        if _valid_cache(value, handler, anonymous, now):
            return value["value"]
        else:
            val = func(self, *args, **kwargs)
            c = Cache()
            # need key, or save will not work
            c.key = k
            c.value = val
            c.expire = now + timedelta(seconds=expire)

            if value:
                c.save(value["_id"])
            else:
                c.insert()

            return val
        
    return decorator(wrapper)


def key_gen(self, key, anonymous, *args, **kwargs):
    code = hashlib.md5()
    code.update(str(key))
    
    # copy args to avoid sort original args
    c = list(args[:])
    # sort c to avoid generate different key when args is the same
    # but sequence is different
    c.sort()
    c = [str(v) for v in c]
    code.update("".join(c))

    c = ["%s=%s" % (k, v) for k, v in kwargs]
    c.sort()
    code.update("".join(c))
    
    if isinstance(self, BaseHandler):
        handler = self
    else:
        handler = getattr(self, "handler")

    # execute cache_pre before get cache_condition
    # so we can construct a complex condition.
    cache_pre = getattr(self, "cache_pre", None)
    if cache_pre:
        cache_pre(*args, **kwargs)
    """
    # cache for every users if anonymous is False
    # 
    if not anonymous and handler.current_user:
        # add userid= prefix to avoid key conflict
        code.update(str("userid=%s" % str(handler.current_user._id)))        
    """    
    page = handler.get_argument("page", "")    
    if page:
        code.update(str("page=%s" % page))
        
    code.update(handler.request.host)
    
    return code.hexdigest(), handler
        
def remove(key):
    """Remove a cache's value."""
    c = Cache()
    v = c.findby_key(key)
    if v:
        c.remove(v["_id"])
        
def _valid_cache(value, handler, anonymous, now):
    if not options.cache_enabled:
        return False
    
    if anonymous and handler.current_user:
        return False
    
    if value:
        if value["expire"] > now:
            return True
        else:
            return False
    else:
        return False    