# -*- coding: utf-8 -*-

from pymongo import Connection
from pymongo.errors import ConnectionFailure
from tornado.options import options

from pagemanage.src.libs.exceptions import DBAuthenticatedError, \
                DBConnectionError, DBAttributeError
from pagemanage.src.db import conn

def connect():
    try:
        con = Connection(host=options.mongodb['host'], port=int(options.mongodb['port']))
    except ConnectionFailure:
        raise DBConnectionError('Unable to connect to MongoDB')

    mongodb = con[options.mongodb['database']]
    auth = mongodb.authenticate(options.mongodb['user'], options.mongodb['password'])
    if not auth:
        raise DBAuthenticatedError('Authentication to MongoDB failed')

    conn.mongodb = mongodb    
    
class MongodbModel(dict):
    def __init__(self, row=None):
        if row is not None:
            assert isinstance(row, dict)
            self["_record"] = row
        else:
            self["_record"] = {}

    @property
    def db(self):
        return getattr(conn.mongodb, self.collection())

    def name(self):
        # the same as collection by default
        return self.collection()

    def collection(self):
        """Database collection name"""
        raise NotImplementedError

    def attributes(self):
        """Define a model's attributes which can be set by __setattr__"""
        raise NotImplementedError

    def record(self):
        return self["_record"]

    def __setattr__(self, key, value):
        if key in self.attributes() or key == "_id":
            self.record()[key] = value
        else:
            raise DBAttributeError("%s attribute does not exist in %s."
                                   % (key, self.name()))

    def __getattr__(self, key):
        if key in self.record():
            return self.record()[key]
        elif key in self.attributes():
            return None
        else:
            raise DBAttributeError("%s attribute does not exist in %s."
                                   % (key, self.name()))
    def insert(self):
        return self.db.insert(self.record())
        
    def save(self, _id=None):
        if _id is not None:
            self._id = _id

        assert self._id is not None, "_id should be set."

        return self.db.save(self.record())

    def remove(self, _id=None):
        if _id is not None:
            self._id = _id

        return self.db.remove(self._id)
    