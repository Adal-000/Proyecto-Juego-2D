from mapas.Validacion import PUNTOS_ELEMENTOS, PUNTOS_MONEDAS, calcular_puntaje_editor, calcular_puntaje_monedas

HERRAMIENTAS = {
    "inicio": {"texto": "Inicio", "color": "#22c55e"},
    "meta": {"texto": "Meta", "color": "#facc15"},
    "bloque": {"texto": "Bloque", "color": "#6b7280"},
    "escalera": {"texto": "Escalera", "color": "#b45309"},
    "enemigo": {"texto": "Enemigo", "color": "#dc2626"},
    "trampa": {"texto": "Trampa", "color": "#7f1d1d"},
    "moneda_bronce": {"texto": "Moneda +50", "color": "#cd7f32"},
    "moneda_oro": {"texto": "Moneda +150", "color": "#facc15"},
    "borrar": {"texto": "Borrar", "color": "#ffffff"},
}


def dibujar_grilla(canvas, columnas, filas, tam_celda, ancho_canvas, alto_canvas):
    """Descripcion: dibuja la grilla base del editor en el canvas.
    Entradas: canvas, columnas, filas, tam_celda, ancho_canvas, alto_canvas.
    Salidas: ninguna; limpia y redibuja el fondo cuadriculado.
    Restricciones: medidas deben ser enteros positivos.
    """
    canvas.delete("all")
    canvas.create_rectangle(0, 0, ancho_canvas, alto_canvas, fill="#dbeafe", outline="")

    for columna in range(columnas + 1):
        x = columna * tam_celda
        canvas.create_line(x, 0, x, alto_canvas, fill="#93c5fd")

    for fila in range(filas + 1):
        y = fila * tam_celda
        canvas.create_line(0, y, ancho_canvas, y, fill="#93c5fd")


def dibujar_celda(canvas, celda, herramienta, tam_celda):
    """Descripcion: dibuja una celda segun la herramienta seleccionada.
    Entradas: canvas, celda (fila/columna), herramienta (str), tam_celda (int).
    Salidas: ninguna; pinta la celda y su marcador de texto.
    Restricciones: herramienta debe existir en HERRAMIENTAS.
    """
    x = celda["columna"] * tam_celda
    y = celda["fila"] * tam_celda
    color = HERRAMIENTAS[herramienta]["color"]
    texto = HERRAMIENTAS[herramienta]["texto"][0]

    canvas.create_rectangle(x + 2, y + 2, x + tam_celda - 2, y + tam_celda - 2, fill=color, outline="#111827", width=2)
    canvas.create_text(x + tam_celda / 2, y + tam_celda / 2, text=texto, font=("Arial", 14, "bold"), fill="#111827")


def redibujar_editor(canvas, mapa_editor, columnas, filas, tam_celda, ancho_canvas, alto_canvas):
    """Descripcion: redibuja por completo el estado actual del mapa en edicion.
    Entradas: canvas, mapa_editor y parametros de grilla.
    Salidas: ninguna; renderiza todos los elementos colocados.
    Restricciones: mapa_editor debe contener las listas y claves esperadas.
    """
    dibujar_grilla(canvas, columnas, filas, tam_celda, ancho_canvas, alto_canvas)

    for celda in mapa_editor["bloques"]:
        dibujar_celda(canvas, celda, "bloque", tam_celda)

    for celda in mapa_editor["escaleras"]:
        dibujar_celda(canvas, celda, "escalera", tam_celda)

    for celda in mapa_editor["enemigos"]:
        dibujar_celda(canvas, celda, "enemigo", tam_celda)

    for celda in mapa_editor["trampas"]:
        dibujar_celda(canvas, celda, "trampa", tam_celda)

    for celda in mapa_editor.get("monedas_bronce", []):
        dibujar_celda(canvas, celda, "moneda_bronce", tam_celda)

    for celda in mapa_editor.get("monedas_oro", []):
        dibujar_celda(canvas, celda, "moneda_oro", tam_celda)

    if mapa_editor["inicio"] is not None:
        dibujar_celda(canvas, mapa_editor["inicio"], "inicio", tam_celda)

    if mapa_editor["meta"] is not None:
        dibujar_celda(canvas, mapa_editor["meta"], "meta", tam_celda)


def texto_estado_editor(mapa_editor):
    """Descripcion: genera el texto de resumen de puntajes del editor.
    Entradas: mapa_editor (dict).
    Salidas: str con resumen de puntos y conteos.
    Restricciones: depende de las reglas de puntaje definidas en Validacion.
    """
    puntos = calcular_puntaje_editor(mapa_editor)
    puntos_monedas = calcular_puntaje_monedas(mapa_editor)
    return (
        f"Puntaje del mapa: {puntos} | Monedas posibles: +{puntos_monedas}\n"
        f"Enemigos: +{PUNTOS_ELEMENTOS['enemigo']} c/u | Trampas: +{PUNTOS_ELEMENTOS['trampa']} c/u\n"
        f"Bronce: +{PUNTOS_MONEDAS['moneda_bronce']} c/u | Oro: +{PUNTOS_MONEDAS['moneda_oro']} c/u\n"
        f"Bloques: {PUNTOS_ELEMENTOS['bloque']} c/u | Escaleras: {PUNTOS_ELEMENTOS['escalera']} c/u"
    )
