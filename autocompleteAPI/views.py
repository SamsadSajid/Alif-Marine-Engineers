# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from officer.models import ProductList
from .serializer import ProductSerializer
from rest_framework import generics
from django.shortcuts import render

# Create your views here.


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def list(request):
    if request.method == 'GET':
        print("ummmmm")
        print(request.GET.get('q'))
        products = ProductList.objects.filter(product_name__icontains=request.GET.get('q'))
        serializer = ProductSerializer(products, many=True)
        serializer_data = serializer.data
        customdata = {'results': serializer_data}
        return JSONResponse(customdata)


# class ProductName(generics.ListAPIView):
#     queryset = ProductList.objects.all()
#     serializer_class = ProductSerializer
