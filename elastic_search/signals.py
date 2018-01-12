from officer.models import ProductList
from django.db.models.signals import post_save
from django.dispatch import receiver


# Signal to save each new blog post instance into ElasticSearch
@receiver(post_save, sender=ProductList)
def index_post(sender, instance, **kwargs):
    print("Debugging in elastic_search "+instance)
    instance.indexing()
