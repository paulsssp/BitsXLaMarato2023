from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from .models import UserModel

@csrf_exempt
def logout(request):
    if (request.method == 'POST'):
        # Check if the user exists
        if (UserModel.objects.filter(username=request.POST.get('username')).exists()):
            # Set the token to false
            obj = UserModel.objects.get(username=request.POST.get('username'))
            obj.logged_in = False
            obj.save()

            data = {'status': 'OK', 'message': 'User logged out'}
            return JsonResponse(data)
        else:
            data = {'status': 'ERROR', 'message': 'User does not exist'}
            return JsonResponse(data)

    else:
        return JsonResponse({'error': 'POST method required'}, status=405)

# Create your views here.
@csrf_exempt
def get_encuesta_pbac(request, user_id):
    if (request.method == 'GET'):
        # Comprobar que el usuario está logged_in
        if (UserModel.objects.filter(id=user_id, logged_in=True).exists()):
            data = {'name': 'Get Encuesta PBAC'}
            return JsonResponse(data)

@csrf_exempt
def get_encuesta_qol(request, user_id):
    if (request.method == 'GET'):
        # Comprobar que el usuario está logged_in
        if (UserModel.objects.filter(id=user_id, logged_in=True).exists()):
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

@csrf_exempt
def login(request):
    if (request.method == 'POST'):
        # Check if the user and password are correct
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the user exists
        if (UserModel.objects.filter(username=username).exists()):
            # Check if the password is correct
            if (UserModel.objects.filter(username=username, password=password).exists()):
                # Set the token to true
                obj = UserModel.objects.get(username=username)
                obj.logged_in = True
                obj.save()

                data = {'status': 'OK', 'message': 'User logged in'}
                return JsonResponse(data)
            else:
                data = {'status': 'ERROR', 'message': 'Wrong password'}
                return JsonResponse(data)
        else:
            data = {'status': 'ERROR', 'message': 'User does not exist'}
            return JsonResponse(data)

    else:
        return JsonResponse({'error': 'POST method required'}, status=405)

@csrf_exempt
def register(request):
    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the user exists
        if (UserModel.objects.filter(username=username).exists()):
            data = {'status': 'ERROR', 'message': 'User already exists'}
            return JsonResponse(data)
        
        # Create an object based on the UserModel class with the data from the request
        obj = UserModel(username=username, password=password, logged_in=False)
        obj.save()

        return JsonResponse({'status': 'OK', 'message': 'User created'})
    
    else:
        return JsonResponse({'error': 'POST method required'}, status=405)