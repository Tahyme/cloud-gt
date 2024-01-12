from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import urllib
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

app = Flask(__name__)
app.config['SECRET_KEY'] = '323b22caac41acbf'

# Configuration d'Elasticsearch
es = Elasticsearch([{'host': 'elasticsearch-backend', 'port': 9200, 'scheme': 'http'}])

# Liste des index à vérifier et initialiser
indexes_to_check = ['locations', 'products', 'movements', 'balances']

for index in indexes_to_check:
    try:
        es.search(index=index, body={'query': {'match_all': {}}})
    except NotFoundError:
        # L'index n'existe pas, créons-le
        es.indices.create(index=index, ignore=400)

from flaskinventory import routes

