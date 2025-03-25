"""
Ejecuta pruebas de rendimiento para comparar las versiones secuencial y paralela del simulador.
Mide y muestra en consola los tiempos de ejecución y el speedup para un tablero grande (1000x1000) y números de procesos.
"""


import time
import numpy as np
from matrix import cargar_tablero_predeterminado
from rules import aplicar_reglas_parciales

from concurrent.futures import ProcessPoolExecutor

#desempaqueta los argumentos para usar executor.map
def aplicar_reglas_desempaquetado(args):
    from rules import aplicar_reglas_parciales
    return aplicar_reglas_parciales(*args)

#calcula la siguiente generacion el parallelo !sin lock
def siguiente_generacion_optimizada(tablero, n_procesos=4):
    filas, cols = tablero.shape
    bloque = filas // n_procesos
    tareas = []

    for i in range(n_procesos):
        inicio = i * bloque
        fin = (i + 1) * bloque if i != n_procesos - 1 else filas
        tareas.append((inicio, fin, tablero, None))

    nueva_gen = np.zeros_like(tablero)

    with ProcessPoolExecutor(max_workers=n_procesos) as executor:
        resultados = executor.map(aplicar_reglas_desempaquetado, tareas)
        for inicio, bloque in resultados:
            nueva_gen[inicio:inicio + bloque.shape[0], :] = bloque

    return nueva_gen


#compara el rendimiento de en parallelo y en seuencial para un tablero muy grande
def comparar_rendimiento(filas=1000, cols=1000, generaciones=20, n_procesos=4):
    from rules import aplicar_reglas_completa

    print("Realizando benchmark...\n")

    tablero = cargar_tablero_predeterminado("random", filas, cols)

    #secuencial
    start = time.perf_counter()
    for _ in range(generaciones):
        _, tablero = aplicar_reglas_completa(0, filas, tablero, None)
    end = time.perf_counter()
    tiempo_secuencial = end - start

    tablero = cargar_tablero_predeterminado("random", filas, cols)

    #paralelo (optimizado)
    start = time.perf_counter()
    for _ in range(generaciones):
        tablero = siguiente_generacion_optimizada(tablero, n_procesos=n_procesos)
    end = time.perf_counter()
    tiempo_paralelo = end - start

    print("\n=== COMPARACIÓN DE RENDIMIENTO ===")
    print(f"[Secuencial] Tiempo: {tiempo_secuencial:.4f} s")
    print(f"[Paralelo ({n_procesos} procesos)] Tiempo: {tiempo_paralelo:.4f} s\n")
    