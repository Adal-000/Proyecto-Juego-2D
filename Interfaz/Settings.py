import json
import os
import tkinter as tk
from tkinter import messagebox

RUTA_CONFIGURACION = os.path.join(os.path.dirname(__file__), "configuracion.json")

CANCIONES = {
    "aventura": {
        "nombre": "Aventura",
        "descripcion": "Ritmo equilibrado para jugar niveles normales.",
        "backend": "beep",
        "intervalos": [780, 780, 1050],
    },
    "rapida": {
        "nombre": "Carrera",
        "descripcion": "Ritmo más rápido para partidas intensas.",
        "backend": "beep",
        "intervalos": [430, 430, 620, 430],
    },
    "tranquila": {
        "nombre": "Exploración",
        "descripcion": "Ritmo lento para diseñar y probar mapas.",
        "backend": "beep",
        "intervalos": [1250, 1600, 1250],
    },
    "retro_winsound": {
        "nombre": "Retro Windows",
        "descripcion": "Melodía WAV generada y reproducida con winsound. Funciona sin instalar paquetes extra en Windows.",
        "backend": "winsound",
        "archivo": "retro_winsound.wav",
        "intervalos": [520, 390, 390, 780],
        "notas": [
            [523.25, 180],
            [659.25, 180],
            [783.99, 180],
            [1046.50, 260],
            [783.99, 160],
            [659.25, 160],
            [587.33, 180],
            [698.46, 220],
            [0, 80],
            [523.25, 180],
            [698.46, 180],
            [880.00, 240],
        ],
    },
}

CONFIGURACION_DEFAULT = {
    "musica_activa": True,
    "cancion": "aventura",
}


def centrar_ventana(ventana, ancho=1150, alto=700):
    """Descripcion: centra una ventana de configuracion en la pantalla.
    Entradas: ventana (Tk/Toplevel), ancho (int), alto (int).
    Salidas: ninguna; actualiza geometria de la ventana.
    Restricciones: ventana debe ser valida y ancho/alto positivos.
    """
    p_ancho = ventana.winfo_screenwidth()
    p_alto = ventana.winfo_screenheight()
    x = (p_ancho - ancho) // 2
    y = (p_alto - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


def cargar_configuracion():
    """Descripcion: carga la configuracion de musica desde archivo JSON.
    Entradas: ninguna.
    Salidas: dict con configuracion consolidada y valida.
    Restricciones: si el archivo no existe o clave no valida, usa valores por defecto.
    """
    if not os.path.exists(RUTA_CONFIGURACION):
        return CONFIGURACION_DEFAULT.copy()

    with open(RUTA_CONFIGURACION, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    configuracion = CONFIGURACION_DEFAULT.copy()
    configuracion.update(datos)

    if configuracion["cancion"] == "retro_pygame":
        configuracion["cancion"] = "retro_winsound"

    if configuracion["cancion"] not in CANCIONES:
        configuracion["cancion"] = CONFIGURACION_DEFAULT["cancion"]

    return configuracion


def guardar_configuracion(configuracion):
    """Descripcion: guarda la configuracion de musica en disco.
    Entradas: configuracion (dict serializable a JSON).
    Salidas: ninguna; escribe el archivo de configuracion.
    Restricciones: configuracion debe incluir claves esperadas por el juego.
    """
    with open(RUTA_CONFIGURACION, "w", encoding="utf-8") as archivo:
        json.dump(configuracion, archivo, indent=4, ensure_ascii=False)


def obtener_configuracion_musica():
    """Descripcion: construye una configuracion de musica lista para jugar.
    Entradas: ninguna.
    Salidas: dict con estado, backend, intervalos, archivo y notas.
    Restricciones: la cancion seleccionada debe existir en CANCIONES.
    """
    configuracion = cargar_configuracion()
    cancion = CANCIONES[configuracion["cancion"]]

    return {
        "activa": configuracion["musica_activa"],
        "clave": configuracion["cancion"],
        "nombre": cancion["nombre"],
        "backend": cancion.get("backend", "beep"),
        "intervalos": cancion["intervalos"],
        "archivo": cancion.get("archivo"),
        "notas": cancion.get("notas", []),
    }


def crear_tarjeta(panel, titulo, descripcion):
    """Descripcion: crea una tarjeta visual reutilizable para ajustes.
    Entradas: panel (tk.Frame), titulo (str), descripcion (str).
    Salidas: tk.Frame de la tarjeta creada.
    Restricciones: se usa dentro de una interfaz Tkinter activa.
    """
    tarjeta = tk.Frame(panel, bg="#1f2937", highlightbackground="#374151", highlightthickness=2)
    tarjeta.pack(fill="x", padx=40, pady=8)

    tk.Label(
        tarjeta,
        text=titulo,
        font=("Arial", 18, "bold"),
        fg="#facc15",
        bg="#1f2937",
        anchor="w",
    ).pack(fill="x", padx=18, pady=(12, 2))

    tk.Label(
        tarjeta,
        text=descripcion,
        font=("Arial", 11),
        fg="#d1d5db",
        bg="#1f2937",
        anchor="w",
        wraplength=820,
        justify="left",
    ).pack(fill="x", padx=18, pady=(0, 12))

    return tarjeta


def settings(ventana_padre=None):
    """Descripcion: abre la ventana de configuracion de musica del juego.
    Entradas: ventana_padre (Tk/Toplevel o None).
    Salidas: ninguna; crea y gestiona la interfaz de ajustes.
    Restricciones: requiere entorno grafico y permisos para leer/escribir configuracion.
    """
    window4 = tk.Toplevel(ventana_padre) if ventana_padre is not None else tk.Tk()
    centrar_ventana(window4)
    window4.title("Settings")
    window4.resizable(False, False)
    window4.configure(bg="#111827")

    configuracion = cargar_configuracion()
    musica_silenciada = tk.BooleanVar(value=not configuracion["musica_activa"])
    cancion_seleccionada = tk.StringVar(value=configuracion["cancion"])

    tk.Label(
        window4,
        text="Configuración de música",
        font=("Arial", 30, "bold"),
        fg="white",
        bg="#111827",
    ).pack(pady=(32, 8))

    tk.Label(
        window4,
        text="Elige una canción para el juego o silencia la música por completo.",
        font=("Arial", 13),
        fg="#d1d5db",
        bg="#111827",
    ).pack(pady=(0, 18))

    panel = tk.Frame(window4, bg="#111827")
    panel.pack(fill="both", expand=True)

    tarjeta_silencio = crear_tarjeta(
        panel,
        "Silencio total",
        "Desactiva todos los sonidos de música del juego. Puedes volver a activar la música cuando quieras.",
    )
    tk.Checkbutton(
        tarjeta_silencio,
        text="Silenciar música por completo",
        variable=musica_silenciada,
        font=("Arial", 12, "bold"),
        fg="white",
        bg="#1f2937",
        selectcolor="#111827",
        activebackground="#1f2937",
        activeforeground="white",
    ).pack(anchor="w", padx=18, pady=(0, 14))

    tarjeta_canciones = crear_tarjeta(
        panel,
        "Canciones disponibles",
        "Selecciona el ritmo que se usará cuando la música esté activa.",
    )

    for clave, datos in CANCIONES.items():
        tk.Radiobutton(
            tarjeta_canciones,
            text=f"{datos['nombre']} - {datos['descripcion']}",
            variable=cancion_seleccionada,
            value=clave,
            font=("Arial", 12),
            fg="white",
            bg="#1f2937",
            selectcolor="#111827",
            activebackground="#1f2937",
            activeforeground="white",
            anchor="w",
        ).pack(fill="x", padx=18, pady=4)

    botones = tk.Frame(window4, bg="#111827")
    botones.pack(pady=24)

    def guardar_actual():
        """Descripcion: guarda la seleccion actual de silencio y cancion.
        Entradas: ninguna.
        Salidas: ninguna; persiste configuracion y muestra confirmacion.
        Restricciones: las variables de control Tk deben estar inicializadas.
        """
        nueva_configuracion = {
            "musica_activa": not musica_silenciada.get(),
            "cancion": cancion_seleccionada.get(),
        }
        guardar_configuracion(nueva_configuracion)
        messagebox.showinfo("Configuración guardada", "La música se actualizará al iniciar o reabrir una partida.")

    tk.Button(
        botones,
        text="Guardar configuración",
        font=("Arial", 13, "bold"),
        bg="#22c55e",
        fg="white",
        width=22,
        command=guardar_actual,
    ).pack(side="left", padx=10)

    tk.Button(
        botones,
        text="Cerrar",
        font=("Arial", 13, "bold"),
        bg="#374151",
        fg="white",
        width=14,
        command=window4.destroy,
    ).pack(side="left", padx=10)

    if ventana_padre is None:
        window4.mainloop()
