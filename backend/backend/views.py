from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.conf import settings
import os


@api_view(['GET'])
def my_data(request):
    data = {
        'message': 'Hello from Django!'
    }
    return Response(data)

def index(request):
    return render(request, 'index.html')

def inventory(request):
    return render(request, 'inventory.html')

def main(request):
    return render(request, 'main.html') 

