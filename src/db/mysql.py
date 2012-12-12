# -*- coding: utf-8 -*-

#from tornado.database import Connection
#from tornado.options import options
#from tornado.ioloop import PeriodicCallback

from pagemanage.src.db import conn

def connect():
    """conn.mysql = Connection(
        host=options.mysql["host"] + ":" + options.mysql["port"],
        database=options.mysql["database"],
        user=options.mysql["user"],
        password=options.mysql["password"])
    """
    # ping db periodically to avoid mysql go away
    #PeriodicCallback(_ping_db, int(options.mysql["recycle"]) * 1000).start()
    pass

def _ping_db():
    # Just a simple query
    #conn.mysql.query("show variables")
    pass