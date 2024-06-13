import numpy as np
import time

# Gauss-Seidel (sumatorias y matrices)
# Matrices
def Gauss_s(A, b, tolerancia):
  xo = [np.zeros(len(b))]
  D = np.diag(np.diag(A))

  L = D - np.tril(A)

  U = D - np.triu(A)

  tiempo_inicial = time.time()
  Tg = np.dot(np.linalg.inv(D - L) , U)

  Cg = np.dot(np.linalg.inv(D - L) , b)

  lam, vec =  np.linalg.eig(Tg)
  radio = max(abs(lam))

  if radio >= 1:
    raise Exception("El método no converge a la solución del sistema")
    return

  contador = 0
  errores = []

  while True:
    contador += 1
    xo.append(np.dot(Tg, xo[-1]) + Cg)# aqui

    error = max(np.abs(xo[-2] - xo[-1]))
    errores.append(error)

    if error <= tolerancia:
      break

  tiempo_final = time.time()
  duracion = tiempo_final - tiempo_inicial

  return xo[-1]

def Gauss_s_sumas(A, b, tol=1e-2):
    n = len(b)
    xo = np.zeros(n)
    x1 = np.zeros(n)

    # Número máximo de iteraciones
    M = 50
    cont = 0

    norm = float('inf')  # Inicializar la norma con un valor grande

    while norm > tol and cont < M:
        for i in range(n):
            aux = 0
            for j in range(n):
                if i != j:
                    aux += A[i, j] * x1[j]  # Utilizar x1 actualizado
            x1[i] = (b[i] - aux) / A[i, i]

        norm = np.max(np.abs(x1 - xo))
        xo = x1.copy()  # Actualizar xo con los nuevos valores de x1
        cont += 1

    return x1



# Eliminación Gaussiana
def eliminacion_gaussiana(A, b):
  A = A.astype(float)  # Convertir A a tipo float
  b = b.astype(float)  # Convertir b a tipo float
  n = len(b)

  for k in range(n-1):
    # Línea de intercambio
    for i in range(k+1, n):
      lam = A[i, k] / A[k,k]
      A[i, k:n] = A[i, k:n] - lam * A[k, k:n]
      b[i] = b[i] - lam * b[k]


  x = np.zeros(n) # Crear un arreglo de n cantidad de ceros
  # Resolver las variables
  for k in range(n-1, -1, -1):
    # Ecuación general que surge de despejar la variable x_k en cada fila
    x[k] = (b[k] - np.dot(A[k, k+1:n], x[k+1:n]))/ A[k, k] # np.dot() producto punto entre dos matrices

  return x


def pivot(A, b):
  A = A.astype(float)
  b = b.astype(float)
  n = len(b)

  for k in range(n - 1):
    # Pivoteo parcial
    max_index = np.argmax(abs(A[k:n, k])) + k
    if A[max_index, k] == 0:
      raise ValueError("El método no converge a la solución del sistema.")

    if max_index != k:
      A[[k, max_index]] = A[[max_index, k]]
      b[[k, max_index]] = b[[max_index, k]]

    for i in range(k + 1, n):
      lam = A[i, k] / A[k, k]
      A[i, k:n] -= lam * A[k, k:n]
      b[i] -= lam * b[k]

  x = np.zeros(n)
  for k in range(n - 1, -1, -1):
    x[k] = (b[k] - np.dot(A[k, k + 1:n], x[k + 1:n])) / A[k, k]

  return x
