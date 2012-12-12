from tornado.options import options

from pagemanage.src.model.access import Access

def callback_job():
    if len(Access.accesses) > options.access_log["valve"]:
        Access().insert_access()
    