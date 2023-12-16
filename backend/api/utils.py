from django.db import models
from django.contrib.auth.models import User

from api.models import CicleMenstrual, DiaMenstrual, EncuestaQOL

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

def calcular_punts_qol(user):
    punts = 0;

    qol = EncuestaQOL.objects.filter(usuari=user).last()

    return (
        qol.mes_7_dies*3 +
        qol.mes_3_dies_abunda*1 +
        qol.regla_molesta*3 +
        qol.mancha_ropa*1 +
        qol.manchar_asiento*1 +
        qol.evitar_activitats*1
    )

def veredicte_qol(user):
    punts = calcular_punts_qol(user)

    if punts > 3:
        return 2
    
    elif punts == 3:
        return 1

    elif punts < 3:
        return 0

def veredicte_pbac(user):
    punts = calcular_punts_test(user)

    if punts > 100:
        return 2
    
    elif punts < 100 and punts > 85:
        return 1

    elif punts < 85:
        return 0