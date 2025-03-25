"""
Muestra gráficamente la evolución del Juego de la Vida usando matplotlib.
Permite visualizar en tiempo real cómo cambia el tablero paso a paso.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button, RadioButtons
from matrix import construir_matriz_paralela, siguiente_generacion_paralela, cargar_tablero_predeterminado

class JuegoDeLaVidaInteractivo:
    def __init__(self, tablero_inicial, generaciones=100, n_procesos=4):
        self.tablero = tablero_inicial.copy()
        self.generaciones = generaciones
        self.generacion_actual = 0
        self.n_procesos = n_procesos
        self.pausado = True

        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.3, right=0.75)
        self.im = self.ax.imshow(self.tablero, cmap='binary', interpolation='nearest')
        self.ax.set_title(f"Generación {self.generacion_actual}")

        #conectar evento de clic para poder dibujar sobre el tablero
        self.cid_click = self.fig.canvas.mpl_connect('button_press_event', self.on_click)

        #botones
        axplay = plt.axes([0.1, 0.15, 0.1, 0.075])
        axpause = plt.axes([0.25, 0.15, 0.1, 0.075])
        axnext = plt.axes([0.4, 0.15, 0.1, 0.075])
        axreset = plt.axes([0.55, 0.15, 0.1, 0.075])
        axradio = plt.axes([0.8, 0.4, 0.15, 0.4])

        self.btn_play = Button(axplay, 'Play')
        self.btn_pause = Button(axpause, 'Pause')
        self.btn_next = Button(axnext, 'Next')
        self.btn_reset = Button(axreset, 'Reset')

        self.radio = RadioButtons(axradio, ('Aleatorio', 'Glider', 'Blinker', 'Diamond', 'Spaceship', 'Bakery', 'Beluchenko', 'Vacio'))

        self.btn_play.on_clicked(self.play)
        self.btn_pause.on_clicked(self.pause)
        self.btn_next.on_clicked(self.next_step)
        self.btn_reset.on_clicked(self.resetear_tablero)
        self.radio.on_clicked(self.seleccionar_patron)

        self.ani = animation.FuncAnimation(self.fig, self.actualizar, interval=300, blit=False, cache_frame_data=False)
        plt.show()

    #botones
    def play(self, event):
        self.pausado = False

    def pause(self, event):
        self.pausado = True

    def next_step(self, event):
        if self.pausado:
            self.tablero = siguiente_generacion_paralela(self.tablero, self.n_procesos)
            self.generacion_actual += 1
            self.im.set_array(self.tablero)
            self.ax.set_title(f"Generación {self.generacion_actual}")
            self.fig.canvas.draw_idle()

    def resetear_tablero(self, event=None):
        self.seleccionar_patron(self.radio.value_selected)

    def seleccionar_patron(self, label):
        filas, cols = self.tablero.shape
        if label == 'Aleatorio':
            self.tablero = construir_matriz_paralela(filas, cols, self.n_procesos)
        elif label == 'Blinker':
            self.tablero = cargar_tablero_predeterminado("blinker", filas, cols)
        elif label == 'Glider':
            self.tablero = cargar_tablero_predeterminado("glider", filas, cols)
        elif label == 'Diamond':
            self.tablero = cargar_tablero_predeterminado("simetrico", filas, cols)
        elif label == 'Spaceship':
            self.tablero = cargar_tablero_predeterminado("spaceship", filas, cols)
        elif label == 'Bakery':
            self.tablero = cargar_tablero_predeterminado("bakery", filas, cols)
        elif label == 'Beluchenko':
            self.tablero = cargar_tablero_predeterminado("beluchenko", filas, cols)
        elif label == "Vacio":
            self.tablero = cargar_tablero_predeterminado("vacio", filas, cols)

        self.generacion_actual = 0
        self.im.set_array(self.tablero)
        self.ax.set_title(f"{self.radio.value_selected} - Generación {self.generacion_actual}")
        self.fig.canvas.draw_idle()

    def actualizar(self, frame):
        if not self.pausado and self.generacion_actual < self.generaciones:
            self.tablero = siguiente_generacion_paralela(self.tablero, self.n_procesos)
            self.generacion_actual += 1
            self.im.set_array(self.tablero)
            self.ax.set_title(f"Generación {self.generacion_actual}")

    def on_click(self, event):
        #solo permitir dibujar si está pausado (para le modo vacio)
        if not self.pausado:
            return
        if event.inaxes != self.ax:
            return
        try:
            fila = int(event.ydata)
            col = int(event.xdata)
            if 0 <= fila < self.tablero.shape[0] and 0 <= col < self.tablero.shape[1]:
                self.tablero[fila, col] = 1 - self.tablero[fila, col]
                self.im.set_array(self.tablero)
                self.fig.canvas.draw_idle()
        except (TypeError, ValueError):
            pass

