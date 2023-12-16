from django.db import models
from .models import UserModel
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from api.models import CicleMenstrual, DiaMenstrual, EncuestaQOL

def calcular_punts_test(user, cicle):
    punts = 0;
    dies = DiaMenstrual.objects.filter(cicle=cicle)

    # Iterem per cada dia del cicle

    for dia in dies:
        punts += (
            dia.compresa_poc_tacada*1 +
            dia.compresa_mitja_tacada*5 + 
            dia.compresa_molt_tacada*20 +
            dia.compresa_coaguls*1 +
            dia.tampo_poc_tacat*1 +
            dia.tampo_mitja_tacat*5 +
            dia.tampo_molt_tacat*10 +
            dia.tampo_coaguls*1
        )
    
    return punts
        

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

def generar_grafic(user):
    usuari_instance = UserModel.objects.get(username=user)
    cicles = CicleMenstrual.objects.filter(usuari=usuari_instance)

    grafic_x = [x for x in range(1, len(cicles)+1)]
    grafic_y = []

    for cicle in cicles:
        grafic_y.append(calcular_punts_test(user, cicle))

    sns.lineplot(x=grafic_x, y=grafic_y, label='Punts al test PBAC')

    plt.axhline(y=300, color='red', linestyle='--', label='Horizontal Line at y=300')
    plt.ylabel('Punts al test PBAC')
    plt.gca().axes.get_xaxis().set_visible(False)

    plt.savefig("grafic.png")