from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.core.serializers import serialize
import json

from .models import CicleMenstrual, DiaMenstrual, UserModel, EncuestaQOL

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
            user_instance = get_object_or_404(UserModel, username=user, logged_in=True)
            data = CicleMenstrual.objects.filter(usuari=user_instance)

            # Return all the DiaMenstual objects grouped by CicleMenstrual
            serialized_data = serialize('json', data)

            # Parse the serialized data
            json_data = json.loads(serialized_data)

            # Group the DiaMenstrual objects by the field you want (replace 'field_name' with the actual field name)
            grouped_data = {}
            for entry in json_data:
                field_value = entry['fields']['field_name']
                grouped_data.setdefault(field_value, []).append(entry['fields'])

            return JsonResponse({'data': grouped_data}, safe=False)
        
        else:
            return JsonResponse({'error': 'User not logged in'}, status=401)

@csrf_exempt
def get_encuesta_qol(request, user):
    if (request.method == 'GET'):
        # Comprobar que el usuario está logged_in
        if (UserModel.objects.filter(username=user, logged_in=True).exists()):
            user_instance = get_object_or_404(UserModel, username=user, logged_in=True)
            data = EncuestaQOL.objects.filter(usuari=user_instance)

            serialized_data = serialize('json', data)

            json_data = [entry['fields'] for entry in json.loads(serialized_data)]
            
            return JsonResponse(json_data, safe=False)
        
        else:
            return JsonResponse({'error': 'User not logged in'}, status=401)

@csrf_exempt
def upload_encuesta_pbac(request):
    if request.method == 'POST':
        username = request.POST.get('usuari')

        # Check if the user is logged in
        user_instance = get_object_or_404(UserModel, username=username, logged_in=True)

        if UserModel.objects.filter(username=username, logged_in=True).exists():
            if request.POST.get('dia') == '1':
                # Create a new CicleMenstrual object
                obj_cicle = CicleMenstrual(usuari=user_instance)
                obj_cicle.save()
            else:
                # Get the last CicleMenstrual object for the user
                obj_cicle = CicleMenstrual.objects.filter(usuari=user_instance).last()
            
            # Create a new DiaMenstrual object
            obj = DiaMenstrual(cicle=obj_cicle, dia=request.POST.get('dia'), compresa_poc_tacada=request.POST.get('compresa_poc_tacada'), compresa_mitja_tacada=request.POST.get('compresa_mitja_tacada'), compresa_molt_tacada=request.POST.get('compresa_molt_tacada'), compresa_coaguls=request.POST.get('compresa_coaguls'), tampo_poc_tacat=request.POST.get('tampo_poc_tacat'), tampo_mitja_tacat=request.POST.get('tampo_mitja_tacat'), tampo_molt_tacat=request.POST.get('tampo_molt_tacat'), tampo_coaguls=request.POST.get('tampo_coaguls'))
            obj.save()
            
            return JsonResponse({'status': 'OK', 'message': 'Encuesta QOL uploaded'})
        else:
            return JsonResponse({'error': 'User not logged in'}, status=401)
    else:
        return JsonResponse({'error': 'POST method required'}, status=405)



@csrf_exempt
def upload_encuesta_qol(request):
    if (request.method == 'POST'):
        # Check if the user is logged in
        if (UserModel.objects.filter(username=request.POST.get('usuari'), logged_in=True).exists()):
            mes_7_dies = request.POST.get('mes_7_dies')
            mes_3_dies_abunda = request.POST.get('mes_3_dies_abunda')
            regla_molesta = request.POST.get('regla_molesta')
            mancha_ropa = request.POST.get('mancha_ropa')
            manchar_asiento = request.POST.get('manchar_asiento')
            evitar_activitats = request.POST.get('evitar_activitats')
            usuari_instance = get_object_or_404(UserModel, username=request.POST.get('usuari'), logged_in=True)
            usuari = usuari_instance

            obj = EncuestaQOL(mes_7_dies=mes_7_dies, mes_3_dies_abunda=mes_3_dies_abunda, regla_molesta=regla_molesta, mancha_ropa=mancha_ropa, manchar_asiento=manchar_asiento, evitar_activitats=evitar_activitats, usuari=usuari)
            obj.save()

            return JsonResponse({'status': 'OK', 'message': 'Encuesta QOL uploaded'})
        
        else:
            return JsonResponse({'error': 'User not logged in'}, status=401)
    
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