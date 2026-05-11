from collections import deque

from mapas.Mapa import (
    VALOR_MONEDA_BRONCE,
    VALOR_MONEDA_ORO,
    crear_bola_fuego,
    crear_lanzador,
    crear_moneda_bronce,
    crear_moneda_oro,
    crear_slime_rojo,
    guardar_mapa_usuario,
)

TAM_CELDA = 40
COLUMNAS = 23
FILAS = 16
ANCHO_CANVAS = COLUMNAS * TAM_CELDA
ALTO_CANVAS = FILAS * TAM_CELDA

PUNTOS_ELEMENTOS = {
    "enemigo": 150,
    "trampa": 200,
    "bloque": -20,
    "escalera": -40,
}

PUNTOS_MONEDAS = {
    "moneda_bronce": VALOR_MONEDA_BRONCE,
    "moneda_oro": VALOR_MONEDA_ORO,
}


def crear_mapa_editor():
    """Descripcion: crea la estructura vacia usada por el editor de mapas.
    Entradas: ninguna.
    Salidas: dict con claves principales del editor.
    Restricciones: se inicializa sin inicio ni meta.
    """
    return {
        "inicio": None,
        "meta": None,
        "bloques": [],
        "escaleras": [],
        "enemigos": [],
        "trampas": [],
        "monedas_bronce": [],
        "monedas_oro": [],
    }


def asegurar_listas_mapa_editor(mapa_editor):
    """Descripcion: garantiza que existan todas las listas requeridas en mapa_editor.
    Entradas: mapa_editor (dict mutable).
    Salidas: ninguna; completa claves faltantes con listas vacias.
    Restricciones: mapa_editor debe ser un diccionario editable.
    """
    for clave in ("bloques", "escaleras", "enemigos", "trampas", "monedas_bronce", "monedas_oro"):
        if clave not in mapa_editor:
            mapa_editor[clave] = []


def calcular_puntaje_editor(mapa_editor):
    """Descripcion: calcula el puntaje base del mapa segun sus elementos.
    Entradas: mapa_editor (dict).
    Salidas: int con puntaje del mapa.
    Restricciones: el resultado nunca baja de 0.
    """
    asegurar_listas_mapa_editor(mapa_editor)
    puntos = 0
    puntos += len(mapa_editor["enemigos"]) * PUNTOS_ELEMENTOS["enemigo"]
    puntos += len(mapa_editor["trampas"]) * PUNTOS_ELEMENTOS["trampa"]
    puntos += len(mapa_editor["bloques"]) * PUNTOS_ELEMENTOS["bloque"]
    puntos += len(mapa_editor["escaleras"]) * PUNTOS_ELEMENTOS["escalera"]

    if puntos < 0:
        puntos = 0

    return puntos


def calcular_puntaje_monedas(mapa_editor):
    """Descripcion: calcula el puntaje adicional potencial por monedas.
    Entradas: mapa_editor (dict).
    Salidas: int con suma de valores de monedas colocadas.
    Restricciones: depende de los valores definidos en PUNTOS_MONEDAS.
    """
    asegurar_listas_mapa_editor(mapa_editor)
    return (
        len(mapa_editor["monedas_bronce"]) * PUNTOS_MONEDAS["moneda_bronce"]
        + len(mapa_editor["monedas_oro"]) * PUNTOS_MONEDAS["moneda_oro"]
    )


def validar_mapa(mapa_editor):
    """Descripcion: valida requisitos minimos y jugabilidad del mapa.
    Entradas: mapa_editor (dict).
    Salidas: lista de errores; vacia si es valido.
    Restricciones: requiere inicio y meta, y un camino alcanzable.
    """
    asegurar_listas_mapa_editor(mapa_editor)
    errores = []

    if mapa_editor["inicio"] is None:
        errores.append("Falta colocar el punto de inicio.")

    if mapa_editor["meta"] is None:
        errores.append("Falta colocar la meta final.")

    if not errores and not validar_alcance_meta(mapa_editor):
        errores.append("No hay un camino válido desde el inicio hasta la meta. Agrega bloques o escaleras para conectar el recorrido.")

    return errores


def celda_a_rectangulo(celda, ancho=TAM_CELDA, alto=TAM_CELDA):
    """Descripcion: transforma una celda de grilla en rectangulo del mundo.
    Entradas: celda (fila/columna), ancho (int), alto (int).
    Salidas: dict con x,y,w,h.
    Restricciones: celda debe incluir fila y columna validas.
    """
    return {
        "x": celda["columna"] * TAM_CELDA,
        "y": celda["fila"] * TAM_CELDA,
        "w": ancho,
        "h": alto,
    }


def crear_enemigo_desde_celda(celda, numero):
    """Descripcion: crea un enemigo alternando subtipo segun indice.
    Entradas: celda (dict), numero (int).
    Salidas: dict de enemigo compatible con el juego.
    Restricciones: usa modulo 3 para rotar entre tipos de enemigo.
    """
    rectangulo = celda_a_rectangulo(celda, 36, 36)

    tipo_enemigo = numero % 3

    if tipo_enemigo == 0:
        return crear_slime_rojo(
            rectangulo["x"] + 2,
            rectangulo["y"] + 4,
            max(0, rectangulo["x"] - 90),
            min(ANCHO_CANVAS, rectangulo["x"] + 140),
        )

    if tipo_enemigo == 1:
        return crear_bola_fuego(
            rectangulo["x"] + 3,
            rectangulo["y"] + 3,
            max(0, rectangulo["y"] - 100),
            min(ALTO_CANVAS, rectangulo["y"] + 140),
        )

    return crear_lanzador(rectangulo["x"] + 1, rectangulo["y"] - 2)


def convertir_a_mapa_juego(mapa_editor):
    """Descripcion: convierte el mapa del editor al formato jugable.
    Entradas: mapa_editor (dict).
    Salidas: dict de mapa listo para iniciar partida.
    Restricciones: inicio y meta deben existir para conversion completa.
    """
    asegurar_listas_mapa_editor(mapa_editor)
    inicio = celda_a_rectangulo(mapa_editor["inicio"])
    meta = celda_a_rectangulo(mapa_editor["meta"], 45, 75)
    bloques = []
    escaleras = []
    enemigos = []
    trampas = []
    monedas = []

    bloques.append({"x": 0, "y": 640, "w": 1150, "h": 60})

    for celda in mapa_editor["bloques"]:
        bloques.append(celda_a_rectangulo(celda))

    for celda in mapa_editor["escaleras"]:
        escaleras.append(celda_a_rectangulo(celda, 40, 80))

    for indice, celda in enumerate(mapa_editor["enemigos"]):
        enemigos.append(crear_enemigo_desde_celda(celda, indice))

    for celda in mapa_editor["trampas"]:
        trampas.append(celda_a_rectangulo(celda))

    for celda in mapa_editor["monedas_bronce"]:
        rectangulo = celda_a_rectangulo(celda, 24, 24)
        monedas.append(crear_moneda_bronce(rectangulo["x"] + 8, rectangulo["y"] + 8))

    for celda in mapa_editor["monedas_oro"]:
        rectangulo = celda_a_rectangulo(celda, 28, 28)
        monedas.append(crear_moneda_oro(rectangulo["x"] + 6, rectangulo["y"] + 6))

    return {
        "inicio": {"x": inicio["x"], "y": inicio["y"]},
        "meta": meta,
        "plataformas": bloques,
        "escaleras": escaleras,
        "enemigos": enemigos,
        "trampas": trampas,
        "monedas": monedas,
        "puntaje_mapa": calcular_puntaje_editor(mapa_editor),
    }


def guardar_mapa(mapa_editor):
    """Descripcion: convierte y guarda un mapa del editor en almacenamiento.
    Entradas: mapa_editor (dict).
    Salidas: dict del mapa convertido.
    Restricciones: delega el guardado en guardar_mapa_usuario.
    """
    mapa_juego = convertir_a_mapa_juego(mapa_editor)
    guardar_mapa_usuario(mapa_juego)

    return mapa_juego


def celdas_iguales(celda1, celda2):
    """Descripcion: compara dos celdas por fila y columna.
    Entradas: celda1 (dict), celda2 (dict).
    Salidas: bool.
    Restricciones: ambas celdas deben tener claves fila y columna.
    """
    return celda1["fila"] == celda2["fila"] and celda1["columna"] == celda2["columna"]


def quitar_celda(lista, celda):
    """Descripcion: elimina una celda objetivo de una lista de celdas.
    Entradas: lista (list), celda (dict).
    Salidas: nueva lista sin la celda indicada.
    Restricciones: usa comparacion por fila y columna.
    """
    return [elemento for elemento in lista if not celdas_iguales(elemento, celda)]


def limpiar_celda(mapa_editor, celda):
    """Descripcion: borra una celda de todas las capas del mapa editor.
    Entradas: mapa_editor (dict), celda (dict).
    Salidas: ninguna; modifica mapa_editor en sitio.
    Restricciones: limpia tambien inicio/meta si coinciden con la celda.
    """
    asegurar_listas_mapa_editor(mapa_editor)
    if mapa_editor["inicio"] is not None and celdas_iguales(mapa_editor["inicio"], celda):
        mapa_editor["inicio"] = None

    if mapa_editor["meta"] is not None and celdas_iguales(mapa_editor["meta"], celda):
        mapa_editor["meta"] = None

    mapa_editor["bloques"] = quitar_celda(mapa_editor["bloques"], celda)
    mapa_editor["escaleras"] = quitar_celda(mapa_editor["escaleras"], celda)
    mapa_editor["enemigos"] = quitar_celda(mapa_editor["enemigos"], celda)
    mapa_editor["trampas"] = quitar_celda(mapa_editor["trampas"], celda)
    mapa_editor["monedas_bronce"] = quitar_celda(mapa_editor["monedas_bronce"], celda)
    mapa_editor["monedas_oro"] = quitar_celda(mapa_editor["monedas_oro"], celda)


def colocar_elemento(mapa_editor, herramienta, celda):
    """Descripcion: coloca un elemento del tipo indicado en una celda.
    Entradas: mapa_editor (dict), herramienta (str), celda (dict).
    Salidas: ninguna; actualiza mapa_editor.
    Restricciones: herramienta debe corresponder a un tipo soportado.
    """
    asegurar_listas_mapa_editor(mapa_editor)
    limpiar_celda(mapa_editor, celda)

    if herramienta == "inicio":
        mapa_editor["inicio"] = celda
    elif herramienta == "meta":
        mapa_editor["meta"] = celda
    elif herramienta == "bloque":
        mapa_editor["bloques"].append(celda)
    elif herramienta == "escalera":
        mapa_editor["escaleras"].append(celda)
    elif herramienta == "enemigo":
        mapa_editor["enemigos"].append(celda)
    elif herramienta == "trampa":
        mapa_editor["trampas"].append(celda)
    elif herramienta == "moneda_bronce":
        mapa_editor["monedas_bronce"].append(celda)
    elif herramienta == "moneda_oro":
        mapa_editor["monedas_oro"].append(celda)


def celda_a_tupla(celda):
    """Descripcion: convierte una celda dict en tupla inmutable.
    Entradas: celda (dict con fila y columna).
    Salidas: tupla (fila, columna).
    Restricciones: requiere claves fila y columna.
    """
    return celda["fila"], celda["columna"]


def celdas_ocupadas_por_escaleras(mapa_editor):
    """Descripcion: calcula el conjunto de celdas ocupadas por escaleras.
    Entradas: mapa_editor (dict).
    Salidas: set de tuplas (fila, columna).
    Restricciones: cada escalera ocupa su celda y la inferior si existe.
    """
    celdas = set()
    for celda in mapa_editor["escaleras"]:
        fila, columna = celda_a_tupla(celda)
        celdas.add((fila, columna))
        if fila + 1 < FILAS:
            celdas.add((fila + 1, columna))
    return celdas


def dentro_del_mapa(posicion):
    """Descripcion: verifica si una posicion cae dentro de la grilla.
    Entradas: posicion (tupla fila, columna).
    Salidas: bool.
    Restricciones: usa limites globales FILAS y COLUMNAS.
    """
    fila, columna = posicion
    return 0 <= fila < FILAS and 0 <= columna < COLUMNAS


def validar_alcance_meta(mapa_editor):
    """Descripcion: comprueba si existe un camino valido de inicio a meta.
    Entradas: mapa_editor (dict).
    Salidas: bool; True cuando la meta es alcanzable.
    Restricciones: considera bloques, peligros, escaleras y saltos limitados.
    """
    asegurar_listas_mapa_editor(mapa_editor)
    if mapa_editor["inicio"] is None or mapa_editor["meta"] is None:
        return False

    inicio = celda_a_tupla(mapa_editor["inicio"])
    meta = celda_a_tupla(mapa_editor["meta"])
    metas = {meta}
    if meta[0] + 1 < FILAS:
        metas.add((meta[0] + 1, meta[1]))

    bloques = {celda_a_tupla(celda) for celda in mapa_editor["bloques"]}
    peligros = {celda_a_tupla(celda) for celda in mapa_editor["trampas"] + mapa_editor["enemigos"]}
    escaleras = celdas_ocupadas_por_escaleras(mapa_editor)
    bloqueados = bloques | peligros

    def es_transitable(posicion):
        """Descripcion: indica si una celda puede recorrerse en la busqueda.
        Entradas: posicion (tupla fila, columna).
        Salidas: bool.
        Restricciones: permite inicio/meta aunque esten en zona bloqueada.
        """
        return dentro_del_mapa(posicion) and (posicion not in bloqueados or posicion in metas or posicion == inicio)

    def tiene_apoyo(posicion):
        """Descripcion: determina si una posicion tiene soporte para avanzar/saltar.
        Entradas: posicion (tupla fila, columna).
        Salidas: bool.
        Restricciones: el apoyo proviene del suelo, bloques o escaleras.
        """
        fila, columna = posicion
        return fila == FILAS - 1 or (fila + 1, columna) in bloques or posicion in escaleras

    visitados = {inicio}
    pendientes = deque([inicio])

    while pendientes:
        posicion = pendientes.popleft()

        if posicion in metas:
            return True

        fila, columna = posicion
        candidatos = []

        if posicion in escaleras:
            candidatos.extend([(fila - 1, columna), (fila + 1, columna)])

        if tiene_apoyo(posicion):
            candidatos.extend([(fila, columna - 1), (fila, columna + 1)])
            for salto_vertical in range(1, 4):
                for salto_horizontal in range(-2, 3):
                    if salto_horizontal != 0 or salto_vertical != 0:
                        candidatos.append((fila - salto_vertical, columna + salto_horizontal))
        else:
            candidatos.append((fila + 1, columna))

        for candidato in candidatos:
            if candidato not in visitados and es_transitable(candidato):
                visitados.add(candidato)
                pendientes.append(candidato)

    return False
