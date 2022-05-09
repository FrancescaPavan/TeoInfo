import numpy as np
import random

from sqlalchemy import false, true

def calc_sig_valor(vAnt):
    m = np.array([[0.5, 0.33, 0],[1,0.66,1],[1,1,1]])
    vAleatorio = random.random()
    for i in range(3):
        if vAleatorio <= m[i,vAnt]:
            return i

def primer_valor():
    vEst = np.array([0.33,0.83,1])
    vAleatorio = random.random()
    for i in range(3):
        if vAleatorio <= vEst[i]:
            return i

def calcular_probabilidades(n,exitos):
    prob=np.array([0.0,0.0,0.0])
    for i in range(3):
        prob[i] = exitos[i]/float(n)
    return prob

def converge(exitos,ant):
    conv = (np.subtract(ant,exitos) < 0.0000001)
    return(np.all(conv))
    
def dos_consecutivos():
    n=0
    exitos=np.array([0,0,0])
    probActual=np.array([0,0,-1])
    probAnterior=np.array([0,0,0])
    vAnterior=primer_valor()
    while not(converge(probActual, probAnterior)) or n < 400000:
        vActual=calc_sig_valor(vAnterior)
        probAnterior = probActual
        n+=1
        if (vAnterior==vActual):
            exitos[vActual] += 1
            probActual = calcular_probabilidades(n,exitos)
        
        vAnterior=vActual
    return probActual

print(dos_consecutivos())