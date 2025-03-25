"""
Contiene funciones para la creación, copia, división y ensamblaje de matrices.
Facilita la manipulación del tablero para la simulación secuencial y paralela.
Crea los patrones escogidos para visualizar el funcionamiento del juego.
"""

import numpy as np
from multiprocessing import Pool, Manager
from rules import aplicar_reglas_parciales, aplicar_reglas_completa

#creacion del tablero con una matriz dividida en bloques
def crear_bloque(args):
    inicio, fin, cols = args
    bloque = np.random.randint(2, size=(fin - inicio, cols))
    return (inicio, bloque)

def construir_matriz_paralela(filas, cols, n_procesos=4):
    bloque = filas // n_procesos
    tareas = []

    for i in range(n_procesos):
        inicio = i * bloque
        fin = (i + 1) * bloque if i != n_procesos - 1 else filas
        tareas.append((inicio, fin, cols))

    with Pool(n_procesos) as pool:
        resultados = pool.starmap(aplicar_reglas_parciales, tareas)

    matriz_final = np.zeros((filas, cols), dtype=int)
    for inicio, bloque in resultados:
        matriz_final[inicio:inicio + bloque.shape[0], :] = bloque

    return matriz_final

#calcula la siguiente generacion en parallelo
def siguiente_generacion_paralela(tablero, n_procesos=4):
    filas, cols = tablero.shape
    bloque = filas // n_procesos
    tareas = []

    manager = Manager()
    lock = manager.Lock()

    for i in range(n_procesos):
        inicio = i * bloque
        fin = (i + 1) * bloque if i != n_procesos - 1 else filas
        tareas.append((inicio, fin, tablero, lock))

    with Pool(processes=n_procesos) as pool:
        resultados = pool.starmap(aplicar_reglas_parciales, tareas)

    nueva_gen = np.zeros_like(tablero)
    for inicio, bloque in resultados:
        nueva_gen[inicio:inicio + bloque.shape[0], :] = bloque

    return nueva_gen

#en secuencial
def siguiente_generacion_secuencial(tablero):
    filas, _ = tablero.shape
    _, nueva_gen = aplicar_reglas_completa(0, filas, tablero, None)
    return nueva_gen


#PATRONES PREDEFINIDOS
def insertar_glider(tablero, x, y):
    if x+3 < tablero.shape[0] and y+3 < tablero.shape[1]:
        tablero[x+1, y+2] = 1
        tablero[x+2, y+3] = 1
        tablero[x+3, y+1] = 1
        tablero[x+3, y+2] = 1
        tablero[x+3, y+3] = 1

def insertar_blinker(tablero, x, y):
    if x < tablero.shape[0] and y+2 < tablero.shape[1]:
        tablero[x, y:y+3] = 1

def insertar_diamond(tablero, centro_fila, centro_columna):
    forma = [4, 6, 8, 10, 12, 10, 8, 6, 4]  # número de células vivas por fila
    inicio_fila = centro_fila - len(forma) // 2
    for i, n in enumerate(forma):
        fila = inicio_fila + i
        if 0 <= fila < tablero.shape[0]:
            inicio_col = centro_columna - n // 2
            fin_col = inicio_col + n
            if 0 <= inicio_col and fin_col <= tablero.shape[1]:
                tablero[fila, inicio_col:fin_col] = 1

def insertar_spaceship_44P5H2V0(tablero, fila_inicio=0, col_inicio=0):
    pattern_coords = [
        (0, 5), (0, 11), 
        (1, 4), (1, 5), (1, 6), (1, 10), (1, 11), (1, 12),
        (2, 3), (2, 6), (2, 10), (2, 13),
        (3, 2), (3, 3), (3, 4), (3, 12), (3, 13), (3, 14),
        (4, 3), (4, 5), (4, 11), (4, 13),
        (5, 5), (5, 6), (5, 10), (5, 11), 
        (6, 1), (6, 6), (6, 10), (6, 15),
        (7, 6), (7, 10),
        (8, 1), (8, 2), (8, 6), (8, 10), (8, 14), (8, 15),
        (9, 3), (9, 6), (9, 10), (9, 13),
        (10, 5), (10, 11)
    ]
    for dx, dy in pattern_coords:
        x = fila_inicio + dx
        y = col_inicio + dy
        if 0 <= x < tablero.shape[0] and 0 <= y < tablero.shape[1]:
            tablero[x, y] = 1

def insertar_bakery(tablero, fila_inicio=0, col_inicio=0):
    pattern_coords = [
        (0, 5), (0, 6),
        (1, 4), (1, 7),
        (2, 4), (2, 6),
        (3, 2), (3, 3), (3, 5), (3, 9),
        (4, 1), (4, 4), (4, 8), (4, 10),
        (5, 1), (5, 3), (5, 7), (5, 10),
        (6, 2), (6, 6), (6, 8), (6, 9),
        (7, 5), (7, 7),
        (8, 4), (8, 7),
        (9, 5), (9, 6)
    ]
    for dx, dy in pattern_coords:
        x = fila_inicio + dx
        y = col_inicio + dy
        if 0 <= x < tablero.shape[0] and 0 <= y < tablero.shape[1]:
            tablero[x, y] = 1

def insertar_beluchenko(tablero, fila_inicio=0, col_inicio=0):
    pattern_coords = [
        (0,16), (0,17), (0,21), (0,22),
        (3,7), (3,8), (3,30), (3,31),
        (4,7), (4,8), (4,30), (4,31),
        (6,4), (6,5), (6,33), (6,34),
        (7,4), (7,5), (7,15), (7,16), (7,22), (7,23), (7,33), (7,34),
        (8,10), (8,11), (8,12), (8,14), (8,15), (8,23), (8,24), (8,26), (8,27), (8,28),
        (9,9), (9,11), (9,27), (9,29),
        (10,9), (10,10), (10,28), (10,29),
        (11,9), (11,29),
        (13,9), (13,29),
        (14,8), (14,9), (14,29), (14,30),
        (15,1), (15,8), (15,30), (15,37),
        (16,1), (16,37),
        (20,1), (20,37),
        (21,1), (21,8), (21,30), (21,37),
        (22,8), (22,9), (22,29), (22,30),
        (23,9), (23,29),
        (25,9), (25,29),
        (26,9), (26,10), (26,28), (26,29),
        (27,9), (27,11), (27,27), (27,29),
        (28,10), (28,11), (28,12), (28,14), (28,15), (28,23), (28,24), (28,26), (28,27), (28,28),
        (29,4), (29,5), (29,15), (29,16), (29,22), (29,23), (29,33), (29,34),
        (30,4), (30,5), (30,33), (30,34),
        (32,7), (32,8), (32,30), (32,31),
        (33,7), (33,8), (33,30), (33,31),
        (36,16), (36,17), (36,21), (36,22),
    ]
    for dx, dy in pattern_coords:
        x = fila_inicio + dx
        y = col_inicio + dy
        if 0 <= x < tablero.shape[0] and 0 <= y < tablero.shape[1]:
            tablero[x, y] = 1


#inicializa un tablero y con un bucle ofrece los diferentes patrones
def cargar_tablero_predeterminado(nombre, filas=100, cols=100):
    tablero = np.zeros((filas, cols), dtype=int)

    if nombre == "vacio":
        return tablero

    elif nombre == "blinker":
        count = 0
        espaciamiento = int(min(filas, cols) / 6)
        for i in range(espaciamiento//2, filas - 5, espaciamiento):
            for j in range(espaciamiento//2, cols - 5, espaciamiento):
                if count >= 36:
                    break
                insertar_blinker(tablero, i, j)
                count += 1
            if count >= 36:
                break

    elif nombre == "glider":
        count = 0
        espaciamiento = int(min(filas, cols) / 5)
        for i in range(0, filas - 20, espaciamiento):
            for j in range(0, cols - 20, espaciamiento):
                if count >= 20:
                    break
                insertar_glider(tablero, i, j)
                count += 1

    elif nombre == "simetrico":
        insertar_diamond(tablero, 12, 12)
        insertar_diamond(tablero, 12, 37)
        insertar_diamond(tablero, 37, 12)
        insertar_diamond(tablero, 37, 37)

    elif nombre == "spaceship":
        insertar_spaceship_44P5H2V0(tablero, 20, 16)

    elif nombre == "bakery":
        insertar_bakery(tablero, filas//2 - 6, cols//2 - 6)

    elif nombre == "beluchenko":
        insertar_beluchenko(tablero, filas//2 - 19, cols//2 - 19)

    else:  # Aleatorio
        tablero = np.random.randint(2, size=(filas, cols))

    return tablero
