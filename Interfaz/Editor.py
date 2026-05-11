import os
import sys
import tkinter as tk
from tkinter import messagebox

RUTA_PROYECTO = os.path.dirname(os.path.dirname(__file__))
if RUTA_PROYECTO not in sys.path:
    sys.path.append(RUTA_PROYECTO)

from mapas.Editor import HERRAMIENTAS, redibujar_editor, texto_estado_editor
from mapas.Validacion import (
    ALTO_CANVAS,
    COLUMNAS,
    FILAS,
    TAM_CELDA,
    ANCHO_CANVAS,
    colocar_elemento,
    crear_mapa_editor,
    guardar_mapa,
    limpiar_celda,
    validar_alcance_meta,
    validar_mapa,
)

ANCHO = 1150
ALTO = 700


def centrar_ventana(ventana, ancho=ANCHO, alto=ALTO):
    """Descripcion: centra y ajusta el tamano de una ventana en la pantalla.
    Entradas: ventana (instancia Tk/Toplevel), ancho (int), alto (int).
    Salidas: ninguna; modifica la geometria de la ventana.
    Restricciones: ancho y alto deben ser positivos; ventana debe exponer metodos de geometria de Tkinter.
    """
    p_ancho = ventana.winfo_screenwidth()
    p_alto = ventana.winfo_screenheight()
    x = (p_ancho - ancho) // 2
    y = (p_alto - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


def actualizar_estado(label_estado, mapa_editor):
    """Descripcion: refresca el texto de estado mostrado en el panel del editor.
    Entradas: label_estado (tk.Label), mapa_editor (dict con estado del mapa).
    Salidas: ninguna; actualiza el texto del label recibido.
    Restricciones: mapa_editor debe cumplir el formato esperado por texto_estado_editor.
    """
    label_estado.config(text=texto_estado_editor(mapa_editor))


def limpiar_todo(mapa_editor):
    """Descripcion: reinicia todos los elementos colocados en el mapa del editor.
    Entradas: mapa_editor (dict editable con claves del mapa).
    Salidas: ninguna; modifica mapa_editor en sitio.
    Restricciones: el diccionario debe contener las claves usadas por el editor.
    """
    mapa_editor["inicio"] = None
    mapa_editor["meta"] = None
    mapa_editor["bloques"] = []
    mapa_editor["escaleras"] = []
    mapa_editor["enemigos"] = []
    mapa_editor["trampas"] = []
    mapa_editor["monedas_bronce"] = []
    mapa_editor["monedas_oro"] = []


def editor(ventana_padre=None):
    """Descripcion: crea y ejecuta la ventana del editor de mapas.
    Entradas: ventana_padre (Tk/Toplevel o None).
    Salidas: ninguna; inicia el flujo visual del editor.
    Restricciones: requiere entorno grafico y modulos de mapas disponibles en el proyecto.
    """
    window3 = tk.Toplevel(ventana_padre) if ventana_padre is not None else tk.Tk()
    centrar_ventana(window3)
    window3.title("Editor de mapas")
    window3.resizable(False, False)
    window3.configure(bg="#111827")

    mapa_editor = crear_mapa_editor()
    estado_editor = {"herramienta": "inicio"}

    panel = tk.Frame(window3, bg="#111827", width=210)
    panel.pack(side="left", fill="y", padx=10, pady=10)

    canvas = tk.Canvas(window3, width=ANCHO_CANVAS, height=ALTO_CANVAS, highlightthickness=0)
    canvas.pack(side="right", padx=10, pady=10)

    tk.Label(panel, text="Editor", font=("Arial", 24, "bold"), fg="white", bg="#111827").pack(pady=8)
    tk.Label(panel, text="Selecciona y da click\nen el mapa", font=("Arial", 11), fg="#d1d5db", bg="#111827").pack(pady=4)

    label_herramienta = tk.Label(panel, text="Herramienta: Inicio", font=("Arial", 12, "bold"), fg="#facc15", bg="#111827")
    label_herramienta.pack(pady=8)

    label_estado = tk.Label(panel, text="", font=("Arial", 9), fg="#e5e7eb", bg="#111827", justify="left")
    label_estado.pack(pady=8)

    def seleccionar(herramienta):
        """Descripcion: cambia la herramienta activa del editor.
        Entradas: herramienta (str, clave valida en HERRAMIENTAS).
        Salidas: ninguna; actualiza estado interno y etiqueta de herramienta.
        Restricciones: herramienta debe existir en HERRAMIENTAS.
        """
        estado_editor["herramienta"] = herramienta
        label_herramienta.config(text=f"Herramienta: {HERRAMIENTAS[herramienta]['texto']}")

    for nombre_herramienta, datos in HERRAMIENTAS.items():
        tk.Button(
            panel,
            text=datos["texto"],
            width=16,
            bg=datos["color"],
            command=lambda herramienta=nombre_herramienta: seleccionar(herramienta),
        ).pack(pady=3)

    def redibujar():
        """Descripcion: vuelve a pintar el canvas y el resumen de estado del mapa.
        Entradas: ninguna.
        Salidas: ninguna; renderiza visualmente el mapa actual.
        Restricciones: canvas y mapa_editor deben estar inicializados.
        """
        redibujar_editor(canvas, mapa_editor, COLUMNAS, FILAS, TAM_CELDA, ANCHO_CANVAS, ALTO_CANVAS)
        actualizar_estado(label_estado, mapa_editor)

    def al_click(evento):
        """Descripcion: procesa un click del usuario para colocar o borrar elementos.
        Entradas: evento (evento de Tkinter con coordenadas x/y).
        Salidas: ninguna; modifica mapa_editor y redibuja el canvas.
        Restricciones: el click debe caer dentro de los limites del mapa para aplicar cambios.
        """
        columna = evento.x // TAM_CELDA
        fila = evento.y // TAM_CELDA

        if columna < 0 or columna >= COLUMNAS or fila < 0 or fila >= FILAS:
            return

        celda = {"fila": fila, "columna": columna}

        if estado_editor["herramienta"] == "borrar":
            limpiar_celda(mapa_editor, celda)
        else:
            colocar_elemento(mapa_editor, estado_editor["herramienta"], celda)

        redibujar()

    def guardar_actual():
        """Descripcion: valida el mapa y lo guarda si cumple las reglas.
        Entradas: ninguna.
        Salidas: dict del mapa de juego guardado o None cuando hay errores.
        Restricciones: el mapa debe pasar validar_mapa para poder guardarse.
        """
        errores = validar_mapa(mapa_editor)

        if errores:
            mensaje = "\n".join(errores)
            label_herramienta.config(text="Corrige el mapa antes de guardar")
            messagebox.showwarning("Mapa incompleto", mensaje)
            return None

        mapa_juego = guardar_mapa(mapa_editor)
        messagebox.showinfo("Mapa guardado", "El mapa creado se guardó. Se conservan los últimos 3 mapas creados y ya puede jugarse.")
        return mapa_juego

    def validar_camino():
        """Descripcion: valida estructura del mapa y alcance desde inicio hasta meta.
        Entradas: ninguna.
        Salidas: ninguna; informa el resultado mediante etiquetas y cuadros de mensaje.
        Restricciones: el mapa debe contener inicio y meta para validar alcance.
        """
        errores = validar_mapa(mapa_editor)

        if errores:
            mensaje = "\n".join(errores)
            label_herramienta.config(text="Mapa no jugable")
            messagebox.showwarning("Validación del camino", mensaje)
        elif validar_alcance_meta(mapa_editor):
            label_herramienta.config(text="Camino válido hasta la meta")
            messagebox.showinfo("Validación del camino", "Sí hay un camino válido desde el inicio hasta la meta.")

    def jugar_mapa():
        """Descripcion: guarda el mapa actual y abre una partida con ese mapa.
        Entradas: ninguna.
        Salidas: ninguna; inicia ventana de juego cuando el mapa es valido.
        Restricciones: depende de guardar_actual y del modulo Jugar.
        """
        from Jugar import jugar

        mapa_juego = guardar_actual()

        if mapa_juego is not None:
            jugar(window3, mapa_juego)

    def borrar_todo():
        """Descripcion: elimina todos los elementos del editor y refresca la vista.
        Entradas: ninguna.
        Salidas: ninguna; limpia el estado del mapa.
        Restricciones: requiere que mapa_editor exista y sea mutable.
        """
        limpiar_todo(mapa_editor)
        redibujar()

    tk.Button(panel, text="Validar camino", width=16, bg="#a78bfa", command=validar_camino).pack(pady=10)
    tk.Button(panel, text="Guardar mapa", width=16, bg="#22c55e", command=guardar_actual).pack(pady=3)
    tk.Button(panel, text="Jugar mapa", width=16, bg="#38bdf8", command=jugar_mapa).pack(pady=3)
    tk.Button(panel, text="Limpiar todo", width=16, bg="#f97316", command=borrar_todo).pack(pady=3)

    canvas.bind("<Button-1>", al_click)
    redibujar()

    if ventana_padre is None:
        window3.mainloop()
