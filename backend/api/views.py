from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.core.serializers import serialize
import json
from . import utils
import io
import seaborn as sns
import matplotlib.pyplot as plt
from .models import CicleMenstrual, DiaMenstrual, EncuestaQOL, UserModel


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
            user_instance = get_object_or_404(
                UserModel, username=user, logged_in=True)
            data = CicleMenstrual.objects.filter(usuari=user_instance)

            # Return all the DiaMenstual objects grouped by CicleMenstrual
            serialized_data = serialize('json', data)

            # Parse the serialized data
            json_data = json.loads(serialized_data)

            # Group the DiaMenstrual objects by the field you want (replace 'field_name' with the actual field name)
            grouped_data = {}
            for entry in json_data:
                field_value = entry['fields']['field_name']
                grouped_data.setdefault(
                    field_value, []).append(entry['fields'])

            return JsonResponse({'data': grouped_data}, safe=False)
            data = {'name': 'Get Encuesta PBAC'}
            return JsonResponse(data)

        else:
            print("no")
            return JsonResponse({'error': 'User not logged in'}, status=401)


@csrf_exempt
def get_encuesta_qol(request, user):
    if (request.method == 'GET'):
        if (request.method == 'GET'):
            # Comprobar que el usuario está logged_in
            if (UserModel.objects.filter(username=user, logged_in=True).exists()):
                user_instance = get_object_or_404(
                    UserModel, username=user, logged_in=True)
                data = EncuestaQOL.objects.filter(usuari=user_instance)

                serialized_data = serialize('json', data)

                json_data = [entry['fields']
                             for entry in json.loads(serialized_data)]

                return JsonResponse(json_data, safe=False)
                data = {'name': 'Get Encuesta QOL'}
                return JsonResponse(data)


@csrf_exempt
def upload_encuesta_pbac(request):
    if request.method == 'POST':
        username = request.POST.get('usuari')

        # Check if the user is logged in
        user_instance = get_object_or_404(
            UserModel, username=username, logged_in=True)

        if request.POST.get('dia') == '1':
            # Create a new CicleMenstrual object
            obj_cicle = CicleMenstrual(usuari=user_instance)
            obj_cicle.save()
        else:
            # Get the last CicleMenstrual object for the user
            obj_cicle = CicleMenstrual.objects.filter(
                usuari=user_instance).last()

        # Create a new DiaMenstrual object
        obj = DiaMenstrual(cicle=obj_cicle, dia=request.POST.get('dia'), punts=request.POST.get('punts'));
        obj.save()

        return JsonResponse({'status': 'OK', 'message': 'Encuesta QOL uploaded'})

@csrf_exempt
def upload_encuesta_qol(request):
        if (request.method == 'POST'):
            data = json.loads(request.body.decode('utf-8'))
            usuari_instance = get_object_or_404(UserModel, username=data.get('usuari'), logged_in=True)
            punts = data.get('punts')
            usuari = usuari_instance

            obj = EncuestaQOL(usuari=usuari, punts=punts)
            obj.save()

            return JsonResponse({'status': 'OK', 'message': 'Encuesta QOL uploaded'})



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

    plt.axhline(y=300, color='red', linestyle='--',
                label='Horizontal Line at y=300')
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
