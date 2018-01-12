from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Search, Integer, Float
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from officer.models import ProductList

# Create a connection to ElasticSearch
connections.create_connection()


# ElasticSearch "model" mapping out what fields to index
class ProductIndex(DocType):
    product_id = Integer()
    product_name = Text()
    slug = Text()
    uploaded_by = Text()
    uploaded_at = Date()
    product_available = Text()
    product_porichiti = Text()
    product_description = Text()
    product_notes = Text()
    product_features = Text()
    quantity = Integer()
    price = Float()

    class Meta:
        index = 'product-index'


# Bulk indexing function, run in shell
def bulk_indexing():
    ProductIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in ProductList.objects.all().iterator()))


# Simple search function
def search(author):
    s = Search().filter('term', author=author)
    response = s.execute()
    return response
