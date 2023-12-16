from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# Create your views here.
@csrf_exempt
def get_encuesta_pbac(request, user_id):
    data = {'name': 'Get Encuesta PBAC'}
    return JsonResponse(data)

@csrf_exempt
def get_encuesta_qol(request, user_id):
    data = {'name': 'Get Encuesta QOL'}
    return JsonResponse(data)

@csrf_exempt
def upload_encuesta_pbac(request):
    if (request.method == 'POST'):
        data = {'name': 'Upload Encuesta PBAC', 'echo': request.POST.get('echo')}
        return JsonResponse(data)
    
    else:
        return JsonResponse({'error': 'POST method required'}, status=405)

@csrf_exempt
def upload_encuesta_qol(request):
    if (request.method == 'POST'):
        data = {'name': 'Upload Encuesta QOL'}
        return JsonResponse(data)
    
    else:
        return JsonResponse({'error': 'POST method required'}, status=405)
