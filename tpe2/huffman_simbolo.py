
import numpy as np
 
arch_beethoven = open("Beethoven", "r")
arch_beethoven_codificado = open("Beethoven_codificado","r+")
arch_lgante = open("L-gante","r")
arch_lgante_codificado = open("L-gante_codificado","r+")

def combinar_datos(text_file):
  text_file.seek(0)
  data = text_file.read()
  data = ''.join(data.split())
  return data


def calcular_distribucion(data):
  cant_total_simbolos = len(data)
  dist_probabilidad = np.array([0,0,0,0,0,0,0,0,0,0])
  for simbolo in data:
    dist_probabilidad[int(simbolo)] += 1
  return dist_probabilidad / cant_total_simbolos

class node:
    def __init__(self, prob, symbol, left=None, right=None):
        self.prob = prob
        self.symbol = symbol
        self.left = left
 
        self.right = right
 
        self.huff = ''
  
def codificar(node,codificacion, val=''):
    
    newVal = val + str(node.huff)
 

    if(node.left):
        codificar(node.left,codificacion, newVal)
    if(node.right):
        codificar(node.right,codificacion, newVal)
 
    
    if(not node.left and not node.right):
        codificacion[node.symbol] = str(newVal)
    return codificacion
      
 
def huffman(dist_probabilidad):
  
 
  nodes = []
  codificacion = np.array(['frafsf','frafsf','frafsf','frafsf','frafsf','frafsf','frafsf','frafsf','frafsf','frafsf'])

  # convierte los simbolos y las frecuencias en nodos del arbol de huffman
  for x in range(len(dist_probabilidad)):
      nodes.append(node(dist_probabilidad[x], x))
 
  while len(nodes) > 1:

      nodes = sorted(nodes, key=lambda x: x.prob)
   
      left = nodes[0]
      right = nodes[1]
   
    
      left.huff = 0
      right.huff = 1

      newNode = node(left.prob+right.prob, left.symbol+right.symbol, left, right)
 

      nodes.remove(left)
      nodes.remove(right)
      nodes.append(newNode)


  return codificar(nodes[0],codificacion)



def escribir_archivo(data_list, arch_codificado, codigo):
  
  for linea in data_list:
    nueva_linea = ''
    for simbolo in linea.strip():
      nueva_linea += codigo[int(simbolo)]
    arch_codificado.write(nueva_linea+'\n')  


def calcular_entropia(dist_probabilidad):
  entropia = 0.0
  for i in range(len(dist_probabilidad)):
    entropia += dist_probabilidad[i] * np.log2(dist_probabilidad[i])
  return -entropia

def calcular_long_media(codigo):
  long = 0.0
  for i in range(len(codigo)):
    long += len(codigo[i])
  return long / len(codigo)

def calcular_rendimiento(codigo, dist_probabilidad):
  return calcular_entropia(dist_probabilidad) / calcular_long_media(codigo)

def mostrarCodificacion(codigo):
  for c in range(len(codigo)):
    print(str(c) + ' -> ' + codigo[c])



def resolver(arch, arch_codificado):
  datos = combinar_datos(arch)
  arch.seek(0)
  data_list = arch.readlines()


  print('distribucion de probabilidades', calcular_distribucion(datos))
  
  codigo = huffman(calcular_distribucion(datos))

  
  escribir_archivo(data_list, arch_codificado, codigo)
# asumimos que los numeros de los archivos sin codificar estan representados en ASCII, por lo que cada simbolo ocupa 8 bits
  print("Longitud en bits original: "+ str(len(datos)))
  
  datos_codificados = combinar_datos(arch_codificado)
  print("Longitud en bits original: "+ str(len(datos_codificados)/8))
  
  print("Codificacion:")
  mostrarCodificacion(codigo)
  print("Rendimiento: " + str(calcular_rendimiento(codigo,calcular_distribucion(datos))))

print("Para el archivo beethoven:")
resolver(arch_beethoven, arch_beethoven_codificado)
print("Para el archivo L-gante:")
resolver(arch_lgante, arch_lgante_codificado)