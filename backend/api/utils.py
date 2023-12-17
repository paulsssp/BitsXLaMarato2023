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
        punts += dia.punts
    
    return punts
        

def calcular_punts_qol(user):
    qol = EncuestaQOL.objects.filter(usuari=user).last()
    return qol.punts


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

