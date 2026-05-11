import os
import sys
import tkinter as tk

RUTA_PROYECTO = os.path.dirname(os.path.dirname(__file__))
if RUTA_PROYECTO not in sys.path:
    sys.path.append(RUTA_PROYECTO)

from jugabilidad.Estado import cargar_mejores_puntajes

ANCHO = 520
ALTO = 440


def centrar_ventana(ventana, ancho=ANCHO, alto=ALTO):
    """Descripcion: centra una ventana de Tkinter en la pantalla.
    Entradas: ventana (Tk/Toplevel), ancho (int), alto (int).
    Salidas: ninguna; ajusta la geometria de la ventana.
    Restricciones: ventana debe ser valida y ancho/alto deben ser positivos.
    """
    p_ancho = ventana.winfo_screenwidth()
    p_alto = ventana.winfo_screenheight()
    x = (p_ancho - ancho) // 2
    y = (p_alto - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


def crear_fila_puntaje(panel, posicion, nombre, puntos):
    """Descripcion: crea una fila visual para mostrar un puntaje en el ranking.
    Entradas: panel (tk.Frame), posicion (int), nombre (str), puntos (int).
    Salidas: ninguna; agrega widgets al panel recibido.
    Restricciones: panel debe pertenecer a una interfaz Tk activa.
    """
    fila = tk.Frame(panel, bg="#1f2937", highlightbackground="#374151", highlightthickness=1)
    fila.pack(fill="x", padx=36, pady=6)

    medalla = "🏆" if posicion == 1 else "⭐"
    texto_posicion = f"{medalla} #{posicion}"

    tk.Label(
        fila,
        text=texto_posicion,
        font=("Arial", 16, "bold"),
        fg="#facc15",
        bg="#1f2937",
        width=8,
        anchor="w",
    ).pack(side="left", padx=(14, 4), pady=12)

    tk.Label(
        fila,
        text=nombre,
        font=("Arial", 15, "bold"),
        fg="white",
        bg="#1f2937",
        anchor="w",
    ).pack(side="left", fill="x", expand=True, padx=8)

    tk.Label(
        fila,
        text=str(puntos),
        font=("Arial", 15, "bold"),
        fg="#22c55e",
        bg="#1f2937",
        width=8,
        anchor="e",
    ).pack(side="right", padx=(4, 14))


def mostrar_puntajes(ventana_padre=None):
    """Descripcion: abre una ventana con los 5 mejores puntajes guardados.
    Entradas: ventana_padre (Tk/Toplevel o None).
    Salidas: ninguna; muestra una ventana con el ranking.
    Restricciones: requiere acceso al archivo de puntajes y entorno grafico.
    """
    ventana = tk.Toplevel(ventana_padre) if ventana_padre is not None else tk.Tk()
    centrar_ventana(ventana)
    ventana.title("Mejores puntajes")
    ventana.resizable(False, False)
    ventana.configure(bg="#111827")

    tk.Label(
        ventana,
        text="Mejores 5 puntajes",
        font=("Arial", 26, "bold"),
        fg="white",
        bg="#111827",
    ).pack(pady=(26, 6))

    tk.Label(
        ventana,
        text="Se guardan automáticamente al ganar una partida.",
        font=("Arial", 11),
        fg="#d1d5db",
        bg="#111827",
    ).pack(pady=(0, 14))

    panel = tk.Frame(ventana, bg="#111827")
    panel.pack(fill="both", expand=True)

    mejores_puntajes = cargar_mejores_puntajes()

    if mejores_puntajes:
        for posicion, (nombre, puntos) in enumerate(mejores_puntajes, start=1):
            crear_fila_puntaje(panel, posicion, nombre, puntos)
    else:
        tk.Label(
            panel,
            text="Todavía no hay puntajes guardados.\n¡Gana una partida para aparecer aquí!",
            font=("Arial", 16, "bold"),
            fg="#d1d5db",
            bg="#111827",
            justify="center",
        ).pack(expand=True)

    tk.Button(
        ventana,
        text="Cerrar",
        font=("Arial", 13, "bold"),
        bg="#374151",
        fg="white",
        width=14,
        command=ventana.destroy,
    ).pack(pady=22)

    if ventana_padre is None:
        ventana.mainloop()
