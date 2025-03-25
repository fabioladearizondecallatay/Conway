"""
Define las reglas del Juego de la Vida de Conway.
Implementa las funciones que determinan la evolución del tablero."""

import numpy as np

#aplicar las reglas del juego por fila
def aplicar_reglas_parciales(inicio, fin, tablero, lock):
    bloque = np.zeros((fin - inicio, tablero.shape[1]), dtype=int)
    
    for i in range(inicio, fin):
        for j in range(tablero.shape[1]):
            vecinos = tablero[max(0, i-1):i+2, max(0, j-1):j+2]
            vivos = np.sum(vecinos) - tablero[i, j]
            if tablero[i, j] == 1 and vivos in [2, 3]:
                bloque[i - inicio, j] = 1
            elif tablero[i, j] == 0 and vivos == 3:
                bloque[i - inicio, j] = 1

    #uso del lock para el ejercicio 
    if lock:
        with lock:
            print(f"[Proceso] Bloque de filas {inicio} a {fin} procesado")
    return (inicio, bloque)

#mismo que aplicar_reglas_parciales pero sobre todo el tablero
def aplicar_reglas_completa(inicio, fin, tablero, lock=None):
    bloque = np.zeros((fin - inicio, tablero.shape[1]), dtype=int)
    
    for i in range(inicio, fin):
        for j in range(tablero.shape[1]):
            vecinos = tablero[max(0, i-1):i+2, max(0, j-1):j+2]
            vivos = np.sum(vecinos) - tablero[i, j]
            if tablero[i, j] == 1 and vivos in [2, 3]:
                bloque[i - inicio, j] = 1
            elif tablero[i, j] == 0 and vivos == 3:
                bloque[i - inicio, j] = 1
    return (inicio, bloque)
