from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    data = {'name': 'Backend Bits Marato'}
    return JsonResponse(data)