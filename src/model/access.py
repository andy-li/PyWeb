# -*- coding: utf-8 -*-

from datetime import datetime

from pagemanage.src.db.mongodb import MongodbModel
from pagemanage.src.db import conn

_collection = "access"

class Access(MongodbModel):
    accesses = []

    def collection(self):
        return _collection

    def attributes(self):
        return ["nickname", "host", "path", "full_url",
                "status_code", "ip", "lang", "agent", "referer",
                "duration", "date"
                ]
        
    def insert_access(self):
        self.db.insert(Access.accesses)
        Access.accesses = []
        
    def logging_access(self, handler):
        now = datetime.now()
        request = handler.request
        user = handler.current_user

        if user is not None:
            nickname = user['nickname']
        else:
            nickname = None

        self.nickname = nickname
        self.host = request.host
        self.path = request.path
        self.full_url = request.full_url()
        self.status_code = handler._status_code
        self.ip = request.remote_ip
        self.lang = request.headers.get("Accept-Language", "en-us,en;q=0.5")
        self.agent = request.headers.get("User-Agent", "Unknown-Agent")
        self.referer = request.headers.get("Referer", None)
        self.duration = 1000.0 * request.request_time() # millisecond
        self.date = now

        self.accesses.append(self.record())

def setup():
    co = getattr(conn.mongodb, _collection)
    co.ensure_index("full_url")
    co.ensure_index("referer")
    co.ensure_index([("date", DESCENDING), ("duration", DESCENDING)])
