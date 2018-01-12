# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json, requests
from officer.models import ProductList, ProductReview
from star_ratings.models import Rating
from cart.forms import CartAddProductForm
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.


def search(request):
    if 'q' in request.GET:
        print(request.GET.get('q'))
        data = {
            "query": {
                "query_string": {"query": request.GET.get('q')}
            }
        }
        response = requests.post('http://127.0.0.1:9200/product-index/product_index/_search',
                                 data=json.dumps(data))
        print (response.json())
        resp = response.json()
        print (resp)
        slug = resp['hits']['hits'][0]['_source']['slug']

        product = get_object_or_404(ProductList, slug=slug)
        product_review = ProductReview.objects.filter(product_id=product.product_id)
        rating_count = Rating.objects.filter(object_id=product.id)
        cart_product_form = CartAddProductForm()

        # product_id = resp['hits']['hits'][0]['_source']['product_id']
        # product_name = resp['hits']['hits'][0]['_source']['product_name']
        # price = resp['hits']['hits'][0]['_source']['price']
        # product_available = resp['hits']['hits'][0]['_source']['product_available']
        # quantity = resp['hits']['hits'][0]['_source']['quantity']
        # product_description = resp['hits']['hits'][0]['_source']['product_description']

        return render(request, 'search/search.html', {
                      'product': product,
                      'product_review': product_review,
                      'rating_count': rating_count,
                      'cart_product_form': cart_product_form,
                      })
