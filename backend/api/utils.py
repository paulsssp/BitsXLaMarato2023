from django.db import models
from django.contrib.auth.models import User

from api.models import CicleMenstrual, DiaMenstrual

def calcular_punts_test(user):
    punts = 0;

    # Agafem l'ultim cicle menstrual
    cicle = CicleMenstrual.objects.filter(usuari=user).last()

    # Agafem els dies del cicle
    dies = DiaMenstrual.objects.filter(cicle=cicle)

    # Iterem per cada dia del cicle

    for dia in dies:
        return (
            dia.compresa_poc_tacada*1 +
            dia.compresa_mitja_tacada*5 + 
            dia.compresa_molt_tacada*20 +
            dia.compresa_coaguls*50 +
            dia.tampo_poc_tacat*1 +
            dia.tampo_mitja_tacat*5 +
            dia.tampo_molt_tacat*10
        )
