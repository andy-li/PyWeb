# -*- coding: utf-8 -*-

import os
from tornado.options import options

from pagemanage.src.libs.importlib import import_module
from pagemanage.src.libs.utils import find_modules

def connect():
    """Connect to databases"""
    from pagemanage.src.db import mongodb, mysql
    mongodb.connect()
    mysql.connect()
    
    # Setup date base(eg. index for the first time)
    if options.setup_db:
        mds = find_modules(os.path.dirname(__file__))
        for m in mds:
            try:
                mod = import_module("." + m, package="pagemanage.src.db")
                setup = getattr(mod, "setup", None)
                if setup is not None:
                    setup()
            except ImportError:
                pass
            
class _Connection(dict):
    def __init__(self):
        self["_db"] = {"mysql":None, "mongodb":None}

    def __getattr__(self, key):
        if key in self["_db"]:
            return self["_db"][key]
        else:
            raise AttributeError

    def __setattr__(self, key, value):
        if key in self["_db"]:
            self["_db"][key] = value
        else:
            raise AttributeError

conn = _Connection()
         