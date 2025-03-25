"""
archivo principal del proyecto:
Permite ejecutar la simulación del Juego de la Vida de Conway en modo secuencial, paralelo o visual.
Recibe parámetros desde la línea de comandos como el tamaño del tablero, número de pasos y procesos.
"""

import time
from matrix import cargar_tablero_predeterminado
from visual import JuegoDeLaVidaInteractivo
from benchmark import comparar_rendimiento

def main():
    comparar_rendimiento() #para ver rapidamente la interfaz interactiva, recomiendo ponerlo como texto porque tarda bastante (30sec a 1min)

    #configuracion del tablero visual
    filas, cols = 50, 50
    generaciones = 200
    n_procesos = 4
    tablero = cargar_tablero_predeterminado("random", filas, cols)

    #inicia la visualización interactiva
    juego = JuegoDeLaVidaInteractivo(tablero, generaciones=generaciones, n_procesos=n_procesos)

if __name__ == "__main__":
    main()