import os
import sys
import time
import tkinter as tk

RUTA_INTERFAZ = os.path.dirname(__file__)
RUTA_PROYECTO = os.path.dirname(RUTA_INTERFAZ)
if RUTA_PROYECTO not in sys.path:
    sys.path.append(RUTA_PROYECTO)
if RUTA_INTERFAZ not in sys.path:
    sys.path.append(RUTA_INTERFAZ)

from jugabilidad.Colisiones import rectangulos_colisionan, revisar_colision_enemigos, revisar_colision_trampas
from jugabilidad.Estado import calcular_puntaje, crear_jugador, guardar_puntaje
from jugabilidad.Movimientos import mover_enemigos
from jugabilidad.Musica import detener_musica_winsound, iniciar_musica_winsound
from mapas.Mapa import ALTO, ALTO_JUGADOR, ANCHO, ANCHO_JUGADOR, crear_mapa_basico, obtener_opciones_mapas, preparar_mapa_para_jugar
from Settings import obtener_configuracion_musica

def centrar_ventana(ventana, ancho=ANCHO, alto=ALTO):
    """Descripcion: centra y dimensiona una ventana de juego en pantalla.
    Entradas: ventana (Tk/Toplevel), ancho (int), alto (int).
    Salidas: ninguna; actualiza la geometria de la ventana.
    Restricciones: ventana valida y dimensiones positivas.
    """
    p_ancho = ventana.winfo_screenwidth()
    p_alto = ventana.winfo_screenheight()
    x = (p_ancho - ancho) // 2
    y = (p_alto - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def crear_texto_resultado(estado, puntos):
    """Descripcion: genera el mensaje final mostrado al terminar la partida.
    Entradas: estado (str), puntos (int).
    Salidas: str con texto de victoria o derrota.
    Restricciones: estado esperado principal es "victoria".
    """
    if estado == "victoria":
        return f"¡Ganaste!\nPuntaje registrado: {puntos}"
    return "Perdiste la partida"

def mostrar_resultado(ventana_juego, estado, puntos):
    """Descripcion: muestra una ventana modal con el resultado de la partida.
    Entradas: ventana_juego (Tk/Toplevel), estado (str), puntos (int).
    Salidas: ninguna; crea interfaz de fin de juego.
    Restricciones: ventana_juego debe estar activa para crear Toplevel.
    """
    resultado = tk.Toplevel(ventana_juego)
    centrar_ventana(resultado, 420, 260)
    resultado.title("Resultado final")
    resultado.resizable(False, False)
    resultado.configure(bg="#171923")

    texto = crear_texto_resultado(estado, puntos)
    tk.Label(
        resultado,
        text=texto,
        font=("Arial", 22, "bold"),
        fg="white",
        bg="#171923",
        justify="center",
    ).pack(expand=True)

    def cerrar_todo():
        """Descripcion: cierra ventana de resultado y partida actual.
        Entradas: ninguna.
        Salidas: ninguna; destruye ambas ventanas.
        Restricciones: solo debe invocarse con ventanas validas.
        """
        resultado.destroy()
        ventana_juego.destroy()

    tk.Button(resultado, text="Volver al menú", font=("Arial", 14), command=cerrar_todo).pack(pady=20)
    resultado.protocol("WM_DELETE_WINDOW", cerrar_todo)
    resultado.grab_set()

def crear_detalle(entidad, canvas_id, coordenadas):
    """Descripcion: registra un detalle grafico asociado a una entidad.
    Entradas: entidad (dict), canvas_id (int), coordenadas (list).
    Salidas: ninguna; agrega metadatos en entidad["detalles"].
    Restricciones: entidad debe ser mutable y representar un objeto dibujable.
    """
    if "detalles" not in entidad:
        entidad["detalles"] = []

    entidad["detalles"].append({
        "canvas_id": canvas_id,
        "coordenadas": coordenadas,
    })

def dibujar_slime_rojo(canvas, enemigo):
    """Descripcion: dibuja un enemigo slime rojo y sus detalles en canvas.
    Entradas: canvas (tk.Canvas), enemigo (dict).
    Salidas: ninguna; actualiza ids y detalles en el diccionario enemigo.
    Restricciones: enemigo debe incluir x, y, w y h.
    """
    enemigo["detalles"] = []
    enemigo["canvas_id"] = canvas.create_oval(
        enemigo["x"],
        enemigo["y"],
        enemigo["x"] + enemigo["w"],
        enemigo["y"] + enemigo["h"],
        fill="#ef4444",
        outline="#7f1d1d",
        width=3,
    )
    enemigo["label_id"] = canvas.create_text(
        enemigo["x"] + enemigo["w"] / 2,
        enemigo["y"] - 14,
        text="SLIME",
        font=("Arial", 8, "bold"),
        fill="#7f1d1d",
    )
    crear_detalle(enemigo, canvas.create_oval(enemigo["x"] + 9, enemigo["y"] + 8, enemigo["x"] + 18, enemigo["y"] + 17, fill="white", outline="#7f1d1d"), [9, 8, 18, 17])
    crear_detalle(enemigo, canvas.create_oval(enemigo["x"] + 25, enemigo["y"] + 8, enemigo["x"] + 34, enemigo["y"] + 17, fill="white", outline="#7f1d1d"), [25, 8, 34, 17])
    crear_detalle(enemigo, canvas.create_oval(enemigo["x"] + 12, enemigo["y"] + 11, enemigo["x"] + 16, enemigo["y"] + 15, fill="#111827", outline=""), [12, 11, 16, 15])
    crear_detalle(enemigo, canvas.create_oval(enemigo["x"] + 28, enemigo["y"] + 11, enemigo["x"] + 32, enemigo["y"] + 15, fill="#111827", outline=""), [28, 11, 32, 15])
    crear_detalle(enemigo, canvas.create_arc(enemigo["x"] + 13, enemigo["y"] + 15, enemigo["x"] + 31, enemigo["y"] + 29, start=200, extent=140, style="arc", outline="#450a0a", width=2), [13, 15, 31, 29])


def dibujar_bola_fuego(canvas, enemigo):
    """Descripcion: dibuja un enemigo bola de fuego y su decoracion.
    Entradas: canvas (tk.Canvas), enemigo (dict).
    Salidas: ninguna; guarda ids de dibujo en enemigo.
    Restricciones: enemigo debe contener dimensiones y posicion validas.
    """
    enemigo["detalles"] = []
    enemigo["canvas_id"] = canvas.create_oval(
        enemigo["x"],
        enemigo["y"],
        enemigo["x"] + enemigo["w"],
        enemigo["y"] + enemigo["h"],
        fill="#f97316",
        outline="#7c2d12",
        width=3,
    )
    enemigo["label_id"] = canvas.create_text(
        enemigo["x"] + enemigo["w"] / 2,
        enemigo["y"] - 14,
        text="FUEGO",
        font=("Arial", 8, "bold"),
        fill="#7c2d12",
    )
    crear_detalle(enemigo, canvas.create_polygon(enemigo["x"] + 17, enemigo["y"] + 2, enemigo["x"] + 29, enemigo["y"] + 19, enemigo["x"] + 17, enemigo["y"] + 33, enemigo["x"] + 5, enemigo["y"] + 19, fill="#facc15", outline="#ea580c"), [17, 2, 29, 19, 17, 33, 5, 19])
    crear_detalle(enemigo, canvas.create_oval(enemigo["x"] + 10, enemigo["y"] + 10, enemigo["x"] + 24, enemigo["y"] + 25, fill="#fff7ed", outline=""), [10, 10, 24, 25])


def dibujar_lanzador(canvas, enemigo):
    """Descripcion: dibuja un lanzador y su proyectil inicial.
    Entradas: canvas (tk.Canvas), enemigo (dict con proyectil).
    Salidas: ninguna; asigna ids de canvas al enemigo y proyectil.
    Restricciones: enemigo debe tener subdict proyectil con dimensiones.
    """
    enemigo["detalles"] = []
    enemigo["canvas_id"] = canvas.create_rectangle(
        enemigo["x"],
        enemigo["y"],
        enemigo["x"] + enemigo["w"],
        enemigo["y"] + enemigo["h"],
        fill="#6d28d9",
        outline="#3b0764",
        width=3,
    )
    enemigo["label_id"] = canvas.create_text(
        enemigo["x"] + enemigo["w"] / 2,
        enemigo["y"] - 14,
        text="LANZA",
        font=("Arial", 8, "bold"),
        fill="#3b0764",
    )
    crear_detalle(enemigo, canvas.create_rectangle(enemigo["x"] + 7, enemigo["y"] + 8, enemigo["x"] + 31, enemigo["y"] + 24, fill="#a78bfa", outline="#3b0764", width=2), [7, 8, 31, 24])
    crear_detalle(enemigo, canvas.create_oval(enemigo["x"] + 13, enemigo["y"] + 13, enemigo["x"] + 25, enemigo["y"] + 25, fill="#111827", outline="#facc15", width=2), [13, 13, 25, 25])
    crear_detalle(enemigo, canvas.create_rectangle(enemigo["x"] + 3, enemigo["y"] + 30, enemigo["x"] + 35, enemigo["y"] + 39, fill="#312e81", outline="#3b0764"), [3, 30, 35, 39])

    proyectil = enemigo["proyectil"]
    proyectil["canvas_id"] = canvas.create_oval(
        proyectil["x"],
        proyectil["y"],
        proyectil["x"] + proyectil["w"],
        proyectil["y"] + proyectil["h"],
        fill="#111827",
        outline="#facc15",
        width=2,
    )


def dibujar_enemigos(canvas, mapa):
    """Descripcion: dibuja todos los enemigos del mapa segun su subtipo.
    Entradas: canvas (tk.Canvas), mapa (dict con enemigos).
    Salidas: ninguna.
    Restricciones: cada enemigo debe tener un subtipo soportado.
    """
    for enemigo in mapa["enemigos"]:
        if enemigo["subtipo"] == "slime_rojo":
            dibujar_slime_rojo(canvas, enemigo)
        elif enemigo["subtipo"] == "bola_fuego":
            dibujar_bola_fuego(canvas, enemigo)
        elif enemigo["subtipo"] == "lanzador":
            dibujar_lanzador(canvas, enemigo)


def dibujar_mapa(canvas, mapa):
    """Descripcion: renderiza fondo, inicio, meta, plataformas y escaleras.
    Entradas: canvas (tk.Canvas), mapa (dict).
    Salidas: ninguna; dibuja elementos estaticos del nivel.
    Restricciones: mapa debe incluir claves inicio, meta, plataformas y escaleras.
    """
    canvas.create_rectangle(0, 0, ANCHO, ALTO, fill="#8ed6ff", outline="")
    canvas.create_text(20, 20, text="← → moverse | Espacio saltar | ↑ ↓ usar escaleras", anchor="nw", font=("Arial", 15, "bold"), fill="#1f2937")

    inicio = mapa["inicio"]
    centro_inicio_x = inicio["x"] + ANCHO_JUGADOR / 2
    centro_inicio_y = inicio["y"] + ALTO_JUGADOR / 2
    canvas.create_oval(centro_inicio_x - 18, centro_inicio_y - 18, centro_inicio_x + 18, centro_inicio_y + 18, fill="#22c55e", outline="#14532d", width=3)
    canvas.create_text(centro_inicio_x, inicio["y"] - 12, text="INICIO", font=("Arial", 10, "bold"), fill="#14532d")

    meta = mapa["meta"]
    poste_x = meta["x"] + 8
    canvas.create_rectangle(poste_x, meta["y"], poste_x + 8, meta["y"] + meta["h"], fill="#78350f", outline="#451a03")
    canvas.create_rectangle(meta["x"] - 8, meta["y"] + meta["h"] - 8, meta["x"] + meta["w"] + 16, meta["y"] + meta["h"] + 4, fill="#92400e", outline="#451a03", width=2)
    canvas.create_polygon(poste_x + 8, meta["y"] + 5, poste_x + 68, meta["y"] + 22, poste_x + 8, meta["y"] + 42, fill="#facc15", outline="#854d0e", width=3)
    canvas.create_polygon(poste_x + 18, meta["y"] + 12, poste_x + 48, meta["y"] + 22, poste_x + 18, meta["y"] + 32, fill="#ef4444", outline="#7f1d1d")
    canvas.create_oval(poste_x - 5, meta["y"] - 9, poste_x + 13, meta["y"] + 9, fill="#fde68a", outline="#854d0e", width=2)
    canvas.create_text(poste_x + 35, meta["y"] - 18, text="META", font=("Arial", 12, "bold"), fill="#854d0e")

    for plataforma in mapa["plataformas"]:
        canvas.create_rectangle(plataforma["x"], plataforma["y"], plataforma["x"] + plataforma["w"], plataforma["y"] + plataforma["h"], fill="#6b7280", outline="#374151", width=2)

    for escalera in mapa["escaleras"]:
        x1 = escalera["x"]
        x2 = escalera["x"] + escalera["w"]
        y1 = escalera["y"]
        y2 = escalera["y"] + escalera["h"]
        canvas.create_line(x1 + 10, y1, x1 + 10, y2, fill="#92400e", width=5)
        canvas.create_line(x2 - 10, y1, x2 - 10, y2, fill="#92400e", width=5)
        y = y1 + 12
        while y < y2:
            canvas.create_line(x1 + 8, y, x2 - 8, y, fill="#b45309", width=4)
            y += 22


def dibujar_monedas(canvas, mapa):
    """Descripcion: dibuja monedas activas y guarda sus ids en cada moneda.
    Entradas: canvas (tk.Canvas), mapa (dict con monedas).
    Salidas: ninguna.
    Restricciones: cada moneda debe incluir subtipo, posicion y dimensiones.
    """
    for moneda in mapa["monedas"]:
        color = "#facc15"
        borde = "#854d0e"
        texto = "+150"

        if moneda["subtipo"] == "moneda_bronce":
            color = "#cd7f32"
            borde = "#78350f"
            texto = "+50"

        moneda["canvas_id"] = canvas.create_oval(
            moneda["x"],
            moneda["y"],
            moneda["x"] + moneda["w"],
            moneda["y"] + moneda["h"],
            fill=color,
            outline=borde,
            width=3,
        )
        moneda["label_id"] = canvas.create_text(
            moneda["x"] + moneda["w"] / 2,
            moneda["y"] - 10,
            text=texto,
            font=("Arial", 8, "bold"),
            fill=borde,
        )


def dibujar_trampas(canvas, mapa):
    """Descripcion: dibuja trampas del mapa como obstaculos peligrosos.
    Entradas: canvas (tk.Canvas), mapa (dict con trampas).
    Salidas: ninguna.
    Restricciones: cada trampa debe contener rectangulo valido.
    """
    for trampa in mapa["trampas"]:
        canvas.create_rectangle(
            trampa["x"],
            trampa["y"],
            trampa["x"] + trampa["w"],
            trampa["y"] + trampa["h"],
            fill="#7f1d1d",
            outline="#450a0a",
            width=2,
        )
        canvas.create_text(
            trampa["x"] + trampa["w"] / 2,
            trampa["y"] + trampa["h"] / 2,
            text="X",
            font=("Arial", 14, "bold"),
            fill="white",
        )


def dibujar_jugador(canvas, jugador):
    """Descripcion: dibuja al jugador y devuelve ids de sus partes visuales.
    Entradas: canvas (tk.Canvas), jugador (dict con posicion/tamano).
    Salidas: dict de ids para actualizar animacion y movimiento.
    Restricciones: jugador debe tener claves x, y, w y h.
    """
    partes = {
        "sombra": canvas.create_oval(jugador["x"] + 2, jugador["y"] + jugador["h"] - 5, jugador["x"] + jugador["w"] - 2, jugador["y"] + jugador["h"] + 3, fill="#6b21a8", outline=""),
        "cuerpo": canvas.create_oval(jugador["x"], jugador["y"] + 8, jugador["x"] + jugador["w"], jugador["y"] + jugador["h"], fill="#8b5cf6", outline="#4c1d95", width=3),
        "cara": canvas.create_oval(jugador["x"] + 6, jugador["y"], jugador["x"] + jugador["w"] - 6, jugador["y"] + 25, fill="#f5d0fe", outline="#4c1d95", width=2),
        "ojo_izq": canvas.create_oval(jugador["x"] + 11, jugador["y"] + 9, jugador["x"] + 15, jugador["y"] + 13, fill="#111827", outline=""),
        "ojo_der": canvas.create_oval(jugador["x"] + 22, jugador["y"] + 9, jugador["x"] + 26, jugador["y"] + 13, fill="#111827", outline=""),
        "brillo": canvas.create_oval(jugador["x"] + 10, jugador["y"] + 29, jugador["x"] + 17, jugador["y"] + 36, fill="#c4b5fd", outline=""),
    }
    return partes


def actualizar_jugador(canvas, jugador, partes):
    """Descripcion: actualiza coordenadas de todas las partes visuales del jugador.
    Entradas: canvas (tk.Canvas), jugador (dict), partes (dict de ids).
    Salidas: ninguna.
    Restricciones: partes debe incluir todos los ids creados por dibujar_jugador.
    """
    canvas.coords(partes["sombra"], jugador["x"] + 2, jugador["y"] + jugador["h"] - 5, jugador["x"] + jugador["w"] - 2, jugador["y"] + jugador["h"] + 3)
    canvas.coords(partes["cuerpo"], jugador["x"], jugador["y"] + 8, jugador["x"] + jugador["w"], jugador["y"] + jugador["h"])
    canvas.coords(partes["cara"], jugador["x"] + 6, jugador["y"], jugador["x"] + jugador["w"] - 6, jugador["y"] + 25)
    canvas.coords(partes["ojo_izq"], jugador["x"] + 11, jugador["y"] + 9, jugador["x"] + 15, jugador["y"] + 13)
    canvas.coords(partes["ojo_der"], jugador["x"] + 22, jugador["y"] + 9, jugador["x"] + 26, jugador["y"] + 13)
    canvas.coords(partes["brillo"], jugador["x"] + 10, jugador["y"] + 29, jugador["x"] + 17, jugador["y"] + 36)


def obtener_mapa_para_jugar(mapa_personalizado):
    """Descripcion: obtiene el mapa jugable base o personalizado.
    Entradas: mapa_personalizado (dict o None).
    Salidas: dict de mapa listo para jugar.
    Restricciones: mapa personalizado debe ser compatible con preparar_mapa_para_jugar.
    """
    if mapa_personalizado is not None:
        return preparar_mapa_para_jugar(mapa_personalizado)

    return crear_mapa_basico()


def texto_boton_musica(estado):
    """Descripcion: genera el texto visible del boton de musica.
    Entradas: estado (dict con musica_activa y nombre_cancion).
    Salidas: str.
    Restricciones: estado debe incluir las claves necesarias.
    """
    if estado["musica_activa"]:
        return f"Detener: {estado['nombre_cancion']}"
    return f"Reanudar: {estado['nombre_cancion']}"


def crear_boton_musica(canvas, estado, reproducir_musica):
    """Descripcion: crea un boton para pausar/reanudar musica en partida.
    Entradas: canvas (tk.Canvas), estado (dict), reproducir_musica (callable).
    Salidas: instancia tk.Button creada.
    Restricciones: detener_musica_winsound debe estar disponible para apagar audio.
    """
    def cambiar_musica():
        """Descripcion: alterna estado de musica y actualiza boton.
        Entradas: ninguna.
        Salidas: ninguna; cambia estado de reproduccion.
        Restricciones: usa el diccionario estado compartido.
        """
        estado["musica_activa"] = not estado["musica_activa"]
        boton_musica.config(text=texto_boton_musica(estado))

        if estado["musica_activa"]:
            reproducir_musica()
        else:
            detener_musica_winsound()
            estado["musica_winsound_activa"] = False

    boton_musica = tk.Button(
        canvas,
        text=texto_boton_musica(estado),
        font=("Arial", 9, "bold"),
        bg="#facc15",
        command=cambiar_musica,
    )
    canvas.create_window(1040, 24, window=boton_musica)

    return boton_musica


def actualizar_puntaje_visible(canvas, texto_puntaje_id, estado, mapa):
    """Descripcion: recalcula y actualiza el texto de puntaje en pantalla.
    Entradas: canvas, texto_puntaje_id, estado (dict), mapa (dict).
    Salidas: ninguna; modifica estado["puntaje_actual"] y label visual.
    Restricciones: requiere inicio_tiempo y puntaje_mapa definidos.
    """
    estado["puntaje_actual"] = calcular_puntaje(estado["inicio_tiempo"], mapa["puntaje_mapa"], estado["puntaje_monedas"])
    canvas.itemconfig(texto_puntaje_id, text=f"Puntaje: {estado['puntaje_actual']}")


def iniciar_juego(ventana_padre=None, mapa_personalizado=None):
    """Descripcion: inicializa una partida completa y su bucle principal.
    Entradas: ventana_padre (Tk/Toplevel o None), mapa_personalizado (dict o None).
    Salidas: ninguna; crea ventana de juego y gestiona eventos.
    Restricciones: requiere entorno grafico y mapa valido.
    """
    ventana = tk.Toplevel(ventana_padre) if ventana_padre is not None else tk.Tk()
    centrar_ventana(ventana)
    ventana.title("Juego - Plataformas")
    ventana.resizable(False, False)

    canvas = tk.Canvas(ventana, width=ANCHO, height=ALTO, highlightthickness=0)
    canvas.pack()

    mapa = obtener_mapa_para_jugar(mapa_personalizado)
    jugador = crear_jugador(mapa["inicio"])
    teclas = {"Left": False, "Right": False, "Up": False, "Down": False, "space": False}
    inicio_tiempo = time.time()
    configuracion_musica = obtener_configuracion_musica()
    estado = {
        "terminado": False,
        "inicio_tiempo": inicio_tiempo,
        "puede_saltar": True,
        "puntaje_actual": calcular_puntaje(inicio_tiempo, mapa["puntaje_mapa"]),
        "puntaje_monedas": 0,
        "musica_activa": configuracion_musica["activa"],
        "nombre_cancion": configuracion_musica["nombre"],
        "backend_musica": configuracion_musica["backend"],
        "configuracion_musica": configuracion_musica,
        "intervalos_musica": configuracion_musica["intervalos"],
        "paso_musica": 0,
        "musica_winsound_activa": False,
    }

    dibujar_mapa(canvas, mapa)
    dibujar_monedas(canvas, mapa)
    dibujar_trampas(canvas, mapa)
    dibujar_enemigos(canvas, mapa)
    partes_jugador = dibujar_jugador(canvas, jugador)
    texto_puntaje_id = canvas.create_text(805, 24, text="Puntaje: 0", font=("Arial", 15, "bold"), fill="#111827")

    def reproducir_musica():
        """Descripcion: reproduce musica segun backend activo y estado actual.
        Entradas: ninguna.
        Salidas: ninguna; programa reproduccion asincrona.
        Restricciones: no se ejecuta cuando el juego termino o musica esta desactivada.
        """
        if estado["terminado"] or not estado["musica_activa"]:
            return

        if estado["backend_musica"] == "winsound":
            if estado["musica_winsound_activa"]:
                return

            configuracion_actual = estado["configuracion_musica"].copy()
            configuracion_actual["activa"] = estado["musica_activa"]
            estado["musica_winsound_activa"] = iniciar_musica_winsound(configuracion_actual)

            if estado["musica_winsound_activa"]:
                return

            estado["backend_musica"] = "beep"

        ventana.bell()
        intervalo = estado["intervalos_musica"][estado["paso_musica"] % len(estado["intervalos_musica"])]
        estado["paso_musica"] += 1
        ventana.after(intervalo, reproducir_musica)

    crear_boton_musica(canvas, estado, reproducir_musica)
    reproducir_musica()

    def presionar(evento):
        """Descripcion: marca una tecla como presionada en el estado de control.
        Entradas: evento de teclado Tk.
        Salidas: ninguna.
        Restricciones: solo procesa teclas registradas en el diccionario teclas.
        """
        if evento.keysym in teclas:
            teclas[evento.keysym] = True

    def soltar(evento):
        """Descripcion: marca una tecla como liberada y rearma salto.
        Entradas: evento de teclado Tk.
        Salidas: ninguna.
        Restricciones: al soltar espacio vuelve a habilitar el salto.
        """
        if evento.keysym in teclas:
            teclas[evento.keysym] = False
        if evento.keysym == "space":
            estado["puede_saltar"] = True

    def esta_en_escalera():
        """Descripcion: comprueba si el jugador esta sobre una escalera.
        Entradas: ninguna.
        Salidas: bool.
        Restricciones: usa un rectangulo central reducido para detectar contacto.
        """
        centro = {"x": jugador["x"] + jugador["w"] / 2 - 3, "y": jugador["y"], "w": 6, "h": jugador["h"]}
        for escalera in mapa["escaleras"]:
            if rectangulos_colisionan(centro, escalera):
                return True
        return False

    def mover_horizontal():
        """Descripcion: actualiza movimiento horizontal y colisiones laterales.
        Entradas: ninguna.
        Salidas: ninguna; modifica posicion x del jugador.
        Restricciones: limita al ancho de pantalla y respeta plataformas.
        """
        jugador["vx"] = 0
        if teclas["Left"]:
            jugador["vx"] = -5
        elif teclas["Right"]:
            jugador["vx"] = 5

        jugador["x"] += jugador["vx"]
        if jugador["x"] < 0:
            jugador["x"] = 0
        if jugador["x"] + jugador["w"] > ANCHO:
            jugador["x"] = ANCHO - jugador["w"]

        for plataforma in mapa["plataformas"]:
            if rectangulos_colisionan(jugador, plataforma):
                if jugador["vx"] > 0:
                    jugador["x"] = plataforma["x"] - jugador["w"]
                elif jugador["vx"] < 0:
                    jugador["x"] = plataforma["x"] + plataforma["w"]

    def mover_vertical():
        """Descripcion: aplica gravedad, escaleras, salto y colisiones verticales.
        Entradas: ninguna.
        Salidas: ninguna; modifica y, vy y en_suelo del jugador.
        Restricciones: al salir por abajo del mapa termina en derrota.
        """
        jugador["en_escalera"] = esta_en_escalera()

        if jugador["en_escalera"]:
            jugador["vy"] = 0
            if teclas["Up"]:
                jugador["y"] -= 4
            elif teclas["Down"]:
                jugador["y"] += 4
        else:
            jugador["vy"] += 0.7
            if jugador["vy"] > 14:
                jugador["vy"] = 14

        if teclas["space"] and jugador["en_suelo"] and estado["puede_saltar"]:
            jugador["vy"] = -13
            jugador["en_suelo"] = False
            estado["puede_saltar"] = False

        jugador["y"] += jugador["vy"]
        jugador["en_suelo"] = False

        for plataforma in mapa["plataformas"]:
            if rectangulos_colisionan(jugador, plataforma):
                if jugador["vy"] >= 0:
                    jugador["y"] = plataforma["y"] - jugador["h"]
                    jugador["vy"] = 0
                    jugador["en_suelo"] = True
                else:
                    jugador["y"] = plataforma["y"] + plataforma["h"]
                    jugador["vy"] = 0

        if jugador["y"] > ALTO:
            terminar("derrota")

    def terminar(resultado):
        """Descripcion: finaliza la partida y muestra pantalla de resultado.
        Entradas: resultado (str, victoria o derrota).
        Salidas: ninguna.
        Restricciones: evita doble ejecucion usando estado["terminado"].
        """
        if estado["terminado"]:
            return
        estado["terminado"] = True
        detener_musica_winsound()
        estado["musica_winsound_activa"] = False
        puntos = 0
        if resultado == "victoria":
            puntos = estado["puntaje_actual"]
            guardar_puntaje("Jugador", puntos)
        mostrar_resultado(ventana, resultado, puntos)

    def revisar_meta():
        """Descripcion: valida si el jugador alcanzo la meta.
        Entradas: ninguna.
        Salidas: ninguna; puede terminar en victoria.
        Restricciones: requiere rectangulo meta valido.
        """
        if rectangulos_colisionan(jugador, mapa["meta"]):
            terminar("victoria")

    def revisar_monedas():
        """Descripcion: detecta monedas recogidas y actualiza puntaje extra.
        Entradas: ninguna.
        Salidas: ninguna; desactiva monedas recolectadas.
        Restricciones: cada moneda debe tener estado activo y ids de canvas.
        """
        for moneda in mapa["monedas"]:
            if moneda["activo"] and rectangulos_colisionan(jugador, moneda):
                moneda["activo"] = False
                estado["puntaje_monedas"] += moneda["valor"]
                canvas.itemconfig(moneda["canvas_id"], state="hidden")
                canvas.itemconfig(moneda["label_id"], state="hidden")

    def revisar_derrota_por_obstaculos():
        """Descripcion: verifica derrota por contacto con enemigos o trampas.
        Entradas: ninguna.
        Salidas: ninguna; puede finalizar la partida.
        Restricciones: depende de funciones de colision externas.
        """
        if revisar_colision_enemigos(jugador, mapa):
            terminar("derrota")
        elif revisar_colision_trampas(jugador, mapa):
            terminar("derrota")

    def cerrar_juego():
        """Descripcion: cierra la ventana del juego y detiene la musica.
        Entradas: ninguna.
        Salidas: ninguna.
        Restricciones: se usa como manejador de cierre de ventana.
        """
        estado["terminado"] = True
        detener_musica_winsound()
        estado["musica_winsound_activa"] = False
        ventana.destroy()

    ventana.protocol("WM_DELETE_WINDOW", cerrar_juego)

    def bucle():
        """Descripcion: ejecuta el ciclo principal de actualizacion del juego.
        Entradas: ninguna.
        Salidas: ninguna; programa la siguiente iteracion cada 16 ms.
        Restricciones: se detiene cuando estado["terminado"] es True.
        """
        if estado["terminado"]:
            return
        mover_horizontal()
        mover_vertical()
        mover_enemigos(canvas, mapa)
        revisar_monedas()
        actualizar_puntaje_visible(canvas, texto_puntaje_id, estado, mapa)
        revisar_derrota_por_obstaculos()
        revisar_meta()
        actualizar_jugador(canvas, jugador, partes_jugador)
        ventana.after(16, bucle)

    ventana.bind("<KeyPress>", presionar)
    ventana.bind("<KeyRelease>", soltar)
    ventana.focus_set()
    bucle()

    if ventana_padre is None:
        ventana.mainloop()


def mostrar_selector_mapas(ventana_padre=None):
    """Descripcion: muestra una ventana para elegir mapa antes de jugar.
    Entradas: ventana_padre (Tk/Toplevel o None).
    Salidas: ninguna; abre selector y lanza juego con la opcion elegida.
    Restricciones: requiere opciones de mapa disponibles.
    """
    selector = tk.Toplevel(ventana_padre) if ventana_padre is not None else tk.Tk()
    centrar_ventana(selector, 520, 440)
    selector.title("Seleccionar mapa")
    selector.resizable(False, False)
    selector.configure(bg="#111827")

    tk.Label(
        selector,
        text="Selecciona un mapa para jugar",
        font=("Arial", 20, "bold"),
        fg="white",
        bg="#111827",
    ).pack(pady=18)

    tk.Label(
        selector,
        text="Siempre está disponible el mapa genérico. También se muestran los últimos 3 mapas creados.",
        font=("Arial", 10),
        fg="#d1d5db",
        bg="#111827",
        wraplength=460,
        justify="center",
    ).pack(pady=4)

    opciones = obtener_opciones_mapas()

    def seleccionar_mapa(mapa):
        """Descripcion: cierra selector e inicia partida con el mapa elegido.
        Entradas: mapa (dict).
        Salidas: ninguna.
        Restricciones: mapa debe ser compatible con iniciar_juego.
        """
        selector.destroy()
        iniciar_juego(ventana_padre, mapa)

    for opcion in opciones:
        texto_boton = f"{opcion['nombre']}\n{opcion['descripcion']}"
        tk.Button(
            selector,
            text=texto_boton,
            width=46,
            height=2,
            bg="#374151",
            fg="white",
            command=lambda mapa=opcion["mapa"]: seleccionar_mapa(mapa),
        ).pack(pady=6)

    tk.Button(selector, text="Cancelar", width=18, command=selector.destroy).pack(pady=14)

    if ventana_padre is None:
        selector.mainloop()


def jugar(ventana_padre=None, mapa_personalizado=None):
    """Descripcion: punto de entrada para jugar mapa personalizado o seleccionado.
    Entradas: ventana_padre (Tk/Toplevel o None), mapa_personalizado (dict o None).
    Salidas: ninguna.
    Restricciones: si no hay mapa_personalizado, abre selector de mapas.
    """
    if mapa_personalizado is not None:
        iniciar_juego(ventana_padre, mapa_personalizado)
    else:
        mostrar_selector_mapas(ventana_padre)
