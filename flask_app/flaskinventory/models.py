from flaskinventory import es
from datetime import datetime
import uuid

class Location:
    def __init__(self, loc_name):
        self.loc_id = str(uuid.uuid4())
        self.loc_name = loc_name

    def save_to_es(self):
        es.index(index='locations', doc_type='_doc', id=self.loc_id, body={
            'loc_name': self.loc_name
        })

class Product:
    def __init__(self, prod_name, prod_qty):
        self.prod_id = str(uuid.uuid4())
        self.prod_name = prod_name
        self.prod_qty = prod_qty

    def save_to_es(self):
        es.index(index='products', doc_type='_doc', id=self.prod_id, body={
            'prod_name': self.prod_name,
            'prod_qty': self.prod_qty
        })

class Movement:
    def __init__(self, ts, frm, to, pname, pqty):
        self.mid = str(uuid.uuid4())
        self.ts = ts
        self.frm = frm
        self.to = to
        self.pname = pname
        self.pqty = pqty

    def save_to_es(self):
        es.index(index='movements', doc_type='_doc', id=self.mid, body={
            'ts': self.ts,
            'frm': self.frm,
            'to': self.to,
            'pname': self.pname,
            'pqty': self.pqty
        })

class Balance:
    def __init__(self, product, location, quantity):
        self.bid = str(uuid.uuid4())
        self.product = product
        self.location = location
        self.quantity = quantity

    def save_to_es(self):
        es.index(index='balances', doc_type='_doc', id=self.bid, body={
            'product': self.product,
            'location': self.location,
            'quantity': self.quantity
        })
