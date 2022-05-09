import numpy as np
import random

def calc_sig_valor(vAnt):
    m = np.array([[0.5, 0.33, 0],[1,0.66,1],[1,1,1]])
    vAleatorio = random.random()
    for i in range(3):
        if vAleatorio <= m[i,vAnt]:
            return i

def calcular_probabilidades(n,exitos):
    prob=np.array([0.0,0.0,0.0])
    for i in range(3):
        prob[i] = exitos[i]/float(n)
    return prob

def converge(prob,ant):
    conv = (np.subtract(ant,prob) < 0.00001)
    return(np.all(conv))

def not_converge_matriz(prob,ant):
    for i in range(3):
        if not(converge(prob[i,:],ant[i,:])):
            return True
    return False

def primer_valor(vEst):
    vAleatorio = random.random()
    for i in range(3):
        if vAleatorio <= vEst[i]:
            return i

def vector_estacionario():
    valor = 0
    n = 1
    exitos = np.array([1,0,0])
    vAnt = np.array([100,0,0])
    vProb = calcular_probabilidades(n,exitos)
    while not(converge(vProb, vAnt)) or n < 10000:
        valor = calc_sig_valor(valor)
        exitos[valor] += 1
        n += 1
        vAnt = vProb
        vProb = calcular_probabilidades(n,exitos)
    vEst = np.array([vProb[0],vProb[0]+vProb[1],vProb[0]+vProb[1]+vProb[2]])
    return vEst

def incrementar_resetear(valor,vContador):
    for i in range(3):
        if i == valor:
            vContador[i] = 0
        else:
            vContador[i] += 1
    return vContador

def calcular_probabilidades_mat(exitos, n):
    prob = np.array([0.0,0.0,0.0,0.0,0.0])
    for i in range(5):
        prob[i] = exitos[i]/n
    return prob

def primera_recurrencia_n_pasos(vEst):
    n = 0
    valor = primer_valor(vEst)
    exitos = np.array([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])
    vContador = np.array([0,0,0])
    vOcurrencias = np.array([0,0,0])
    vOcurrencias[valor] += 1
    prob = np.array([[0.0,0.0,0.0,0.0,0.0],[0.0,0.0,.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0]])
    probAnt = np.array([[100.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0]])
    while (not_converge_matriz(prob,probAnt) or n < 10000):
        valor = calc_sig_valor(valor)
        n += 1
        if vContador[valor] < 5:
            exitos[valor,vContador[valor]] += 1
        vOcurrencias[valor] += 1
        vContador = incrementar_resetear(valor,vContador)
        probAnt = prob
        prob[valor] = calcular_probabilidades_mat(exitos[valor,:], vOcurrencias[valor])
    return prob

vEst = vector_estacionario()
prob = primera_recurrencia_n_pasos(vEst)
for i in range(3):
    print("Probabilidad de primera recurrencia de "+str(i)+" en")
    for j in range(5):
        print("     "+str(j+1)+" pasos: "+str(prob[i,j]))