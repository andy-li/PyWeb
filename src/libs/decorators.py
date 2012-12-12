# -*- coding: utf-8 -*-

import functools
import urllib
from tornado.web import HTTPError
from tornado.options import options

def authenticated(method):
    """Decorate methods with this to require that the user be logged in.
    
    Fix the redirect url with full_url. 
    Tornado use uri by default.
    
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method == "GET":
                url = self.get_login_url()
                if "?" not in url:
                    url += "?" + urllib.urlencode(dict(next=self.request.full_url()))
                self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper
