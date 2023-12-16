from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from . import utils
import io
import seaborn as sns 
import matplotlib.pyplot as plt
from .models import CicleMenstrual, UserModel

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
def get_encuesta_pbac(request, user):
    if (request.method == 'GET'):
        # Comprobar que el usuario está logged_in
        if (UserModel.objects.filter(username=user, logged_in=True).exists()):
            data = {'name': 'Get Encuesta PBAC'}
            return JsonResponse(data)
        
        else:
            print("no")
            return JsonResponse({'error': 'User not logged in'}, status=401)

@csrf_exempt
def get_encuesta_qol(request, user):
    if (request.method == 'GET'):
        # Comprobar que el usuario está logged_in
        if (UserModel.objects.filter(username=user, logged_in=True).exists()):
            data = {'name': 'Get Encuesta QOL'}
            return JsonResponse(data)
        
        else:
            return JsonResponse({'error': 'User not logged in'}, status=401)

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
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')

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

@csrf_exempt
def test(request):
    print(utils.generar_grafic("paulita"))
    return JsonResponse({'status': 'OK', 'message': 'Test'})

@csrf_exempt
def grafic_pbac(request, user):
    usuari_instance = UserModel.objects.get(username=user)
    cicles = CicleMenstrual.objects.filter(usuari=usuari_instance)

    grafic_x = [x for x in range(1, len(cicles)+1)]
    grafic_y = []

    for cicle in cicles:
        grafic_y.append(utils.calcular_punts_test(user, cicle))

    sns.lineplot(x=grafic_x, y=grafic_y, label='Punts al test PBAC')

    plt.axhline(y=300, color='red', linestyle='--', label='Horizontal Line at y=300')
    plt.ylabel('Punts al test PBAC')
    plt.gca().axes.get_xaxis().set_visible(False)

    plt.savefig("grafic.png")

    image_buffer = io.BytesIO()
    plt.savefig(image_buffer, format='png')
    plt.close()

    # Move the buffer cursor to the beginning to read all the data
    image_buffer.seek(0)

    # Return the image as HttpResponse
    return HttpResponse(image_buffer.read(), content_type='image/png')
    