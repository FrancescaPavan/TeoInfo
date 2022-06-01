import numpy as np
arch_beethoven = open("Beethoven", "r")
arch_beethoven_codificado = open("Beethoven_codificado","r+")
arch_lgante = open("L-gante","r")
arch_lgante_codificado = open("L-gante_codificado","r+")

# clase que define la estructura de un nodo del arbol de huffman
class nodo:
    def __init__(self, prob, simbolo, izq=None, der=None):
        self.prob = prob
        self.simbolo = simbolo
        self.izq = izq
        self.der = der
        self.huff = ''
      
# formatea los datos como un string
def combinar_datos(text_file):
  text_file.seek(0)
  data = text_file.read()
  data = ''.join(data.split())
  return data

# devuelve un diccionario con las probabilidades de cada simbolo
def calcular_distribucion(data_list):
  cant_total_simbolos = len(data_list)
  distribucion = dict()
  for linea in data_list:
    line = linea.strip()
    valor = distribucion.get(line,-1)
    if (valor == -1): #o sea que no esta el simbolo en el dict
      distribucion.update({line:1})
    else:
      valor += 1
      distribucion.update({line: valor})
  for key in distribucion:
    ocurrencias = distribucion.get(key)
    distribucion.update({key:(ocurrencias/cant_total_simbolos)})
  return distribucion

#  recorre el arbol de huffman para armar un diccionario con el codigo
def codificar(nodo,codificacion, val=''):
    newVal = val + str(nodo.huff)
    if(nodo.izq):
        codificar(nodo.izq,codificacion, newVal)
    if(nodo.der):
        codificar(nodo.der,codificacion, newVal)
    if(not nodo.izq and not nodo.der):
        codificacion.update({nodo.simbolo:newVal})
    return codificacion

# devuleve un diccionario con el codigo
def huffman(dist_probabilidad):
  nodes = []
  codificacion = dict()
  # convierte los simbolos y las frecuencias en nodos del arbol de huffman
  for key in dist_probabilidad:
    nodes.append(nodo(dist_probabilidad.get(key),key))
  while len(nodes) > 1:
      nodes = sorted(nodes, key=lambda x: x.prob)   
      izq = nodes[0]
      der = nodes[1]   
      izq.huff = 0
      der.huff = 1
      newNode = nodo(izq.prob+der.prob, izq.simbolo+der.simbolo, izq, der)
      nodes.remove(izq)
      nodes.remove(der)
      nodes.append(newNode)
  return codificar(nodes[0],codificacion)

# usa el codigo obtenido para traducir el archivo original
def escribir_archivo(data_list, arch_codificado, codigo):
  for linea in data_list:
    line = str(linea).rstrip('\n')
    codificado = codigo.get(line)
    arch_codificado.write(codificado)

def calcular_entropia(dist_probabilidad):
  entropia = 0.0
  for key in dist_probabilidad:
    entropia += dist_probabilidad.get(key) * np.log2(dist_probabilidad.get(key))
  return -entropia

def calcular_long_media(codigo):
  long = 0.0
  for key in codigo:
    long += len(codigo.get(key))
  return long / len(codigo)

def calcular_rendimiento(dist_probabilidad,codigo):
  return calcular_entropia(dist_probabilidad) / calcular_long_media(codigo)

def resolver(arch,arch_codificado):
  data_list = arch.readlines()
  codigo = dict()
  distribucion_probabilidades = calcular_distribucion(data_list)
  codigo = huffman(distribucion_probabilidades)
  
  escribir_archivo(data_list, arch_codificado, codigo)
  print("Entropia: "+str(calcular_entropia(distribucion_probabilidades)))
  print("Longitud media de codigo: "+str(calcular_long_media(codigo)))
  print("Rendimiento "+str(calcular_rendimiento(distribucion_probabilidades,codigo)))
  
  # asumimos que los numeros de los archivos sin codificar estan representados en ASCII, por lo que cada simbolo ocupa 1 byte
  tamano_original = len(combinar_datos(arch))
  tamano_codificado = len(combinar_datos(arch_codificado))/8
  mejora = tamano_original/tamano_codificado
  print("Tamano del archivo original en bytes: "+str(tamano_original))
  print("Tamano del archivo codificado en bytes: "+str(tamano_codificado))
  print("Mejora de codificacion: "+ str(mejora))

print("\n ******** \n")
print("Resolucion para el archivo de Beethoven")
resolver(arch_beethoven,arch_beethoven_codificado)
print("\n ******** \n")
print("Resolucion para el archivo de L-gante")
resolver(arch_lgante,arch_lgante_codificado)
print("\n ******** \n")
