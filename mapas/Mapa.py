import copy
import json
import os
import time

ANCHO = 1150
ALTO = 700
SUELO = 640
ANCHO_JUGADOR = 36
ALTO_JUGADOR = 44
RUTA_MAPA_CREADO = os.path.join(os.path.dirname(__file__), "mapa_creado.json")
RUTA_MAPAS_USUARIO = os.path.join(os.path.dirname(__file__), "mapas_creados.json")
CANTIDAD_MAXIMA_MAPAS = 3
VALOR_MONEDA_BRONCE = 50
VALOR_MONEDA_ORO = 150


def crear_mapa_basico():
    """Descripcion: construye el mapa generico por defecto del juego.
    Entradas: ninguna.
    Salidas: dict con inicio, meta, plataformas, enemigos y monedas.
    Restricciones: usa constantes globales de dimensiones del proyecto.
    """
    return {
        "inicio": {"x": 80, "y": SUELO - ALTO_JUGADOR},
        "meta": {"x": 1040, "y": 190, "w": 45, "h": 75},
        "plataformas": [
            {"x": 0, "y": SUELO, "w": ANCHO, "h": 60},
            {"x": 170, "y": 535, "w": 210, "h": 25},
            {"x": 465, "y": 445, "w": 240, "h": 25},
            {"x": 790, "y": 350, "w": 230, "h": 25},
            {"x": 990, "y": 270, "w": 120, "h": 25},
        ],
        "escaleras": [
            {"x": 250, "y": 385, "w": 55, "h": 150},
            {"x": 575, "y": 295, "w": 55, "h": 150},
            {"x": 910, "y": 270, "w": 55, "h": 80},
        ],
        "trampas": [],
        "monedas": [
            crear_moneda_bronce(330, 500),
            crear_moneda_bronce(615, 410),
            crear_moneda_oro(1010, 225),
        ],
        "puntaje_mapa": 0,
        "enemigos": [
            crear_slime_rojo(405, SUELO - 34, 360, 560),
            crear_bola_fuego(735, 395, 300, 505),
            crear_lanzador(820, 308),
        ],
    }


def crear_slime_rojo(x, y, limite_izquierdo=None, limite_derecho=None):
    """Descripcion: crea la estructura de un enemigo tipo slime rojo.
    Entradas: x, y y limites opcionales de patrulla horizontal.
    Salidas: dict de enemigo inicializado.
    Restricciones: los limites deben cubrir el ancho del enemigo.
    """
    if limite_izquierdo is None:
        limite_izquierdo = x - 90

    if limite_derecho is None:
        limite_derecho = x + 140

    return {
        "nombre": "Slime Rojo",
        "subtipo": "slime_rojo",
        "x": x,
        "y": y,
        "w": 42,
        "h": 34,
        "vx": 2.2,
        "vy": 0,
        "limite_izquierdo": limite_izquierdo,
        "limite_derecho": limite_derecho,
        "canvas_id": None,
        "label_id": None,
        "activo": True,
    }


def crear_bola_fuego(x, y, limite_superior=None, limite_inferior=None):
    """Descripcion: crea la estructura de un enemigo tipo bola de fuego.
    Entradas: x, y y limites opcionales de movimiento vertical.
    Salidas: dict de enemigo inicializado.
    Restricciones: los limites deben permitir el alto del enemigo.
    """
    if limite_superior is None:
        limite_superior = y - 100

    if limite_inferior is None:
        limite_inferior = y + 140

    return {
        "nombre": "Bola de Fuego",
        "subtipo": "bola_fuego",
        "x": x,
        "y": y,
        "w": 34,
        "h": 34,
        "vx": 0,
        "vy": 2.8,
        "limite_superior": limite_superior,
        "limite_inferior": limite_inferior,
        "canvas_id": None,
        "label_id": None,
        "activo": True,
    }


def crear_lanzador(x, y):
    """Descripcion: crea un enemigo lanzador con proyectil asociado.
    Entradas: x (int), y (int).
    Salidas: dict de enemigo con subestructura proyectil.
    Restricciones: la posicion debe quedar dentro del area jugable.
    """
    return {
        "nombre": "Lanzador",
        "subtipo": "lanzador",
        "x": x,
        "y": y,
        "w": 38,
        "h": 42,
        "vx": 0,
        "vy": 0,
        "canvas_id": None,
        "label_id": None,
        "activo": True,
        "proyectil": {
            "x": x - 18,
            "y": y + 15,
            "w": 16,
            "h": 12,
            "vx": -4,
            "vy": 0,
            "inicio_x": x - 18,
            "distancia": 260,
            "canvas_id": None,
            "activo": True,
        },
    }


def crear_moneda_bronce(x, y):
    """Descripcion: crea una moneda de bronce coleccionable.
    Entradas: x (int), y (int).
    Salidas: dict de moneda activa.
    Restricciones: valor fijo segun VALOR_MONEDA_BRONCE.
    """
    return {
        "nombre": "Moneda Bronce",
        "subtipo": "moneda_bronce",
        "x": x,
        "y": y,
        "w": 24,
        "h": 24,
        "valor": VALOR_MONEDA_BRONCE,
        "canvas_id": None,
        "label_id": None,
        "activo": True,
    }


def crear_moneda_oro(x, y):
    """Descripcion: crea una moneda de oro coleccionable.
    Entradas: x (int), y (int).
    Salidas: dict de moneda activa.
    Restricciones: valor fijo segun VALOR_MONEDA_ORO.
    """
    return {
        "nombre": "Moneda Oro",
        "subtipo": "moneda_oro",
        "x": x,
        "y": y,
        "w": 28,
        "h": 28,
        "valor": VALOR_MONEDA_ORO,
        "canvas_id": None,
        "label_id": None,
        "activo": True,
    }


def preparar_mapa_para_jugar(mapa):
    """Descripcion: normaliza un mapa para uso en tiempo de juego.
    Entradas: mapa (dict de origen).
    Salidas: copia profunda del mapa con campos faltantes completados.
    Restricciones: requiere estructura compatible con las claves principales del juego.
    """
    mapa_juego = copy.deepcopy(mapa)

    if "plataformas" not in mapa_juego:
        mapa_juego["plataformas"] = []
    if "escaleras" not in mapa_juego:
        mapa_juego["escaleras"] = []
    if "enemigos" not in mapa_juego:
        mapa_juego["enemigos"] = []
    if "trampas" not in mapa_juego:
        mapa_juego["trampas"] = []
    if "monedas" not in mapa_juego:
        mapa_juego["monedas"] = []
    if "puntaje_mapa" not in mapa_juego:
        mapa_juego["puntaje_mapa"] = 0

    for moneda in mapa_juego["monedas"]:
        moneda["canvas_id"] = None
        moneda["label_id"] = None
        moneda["activo"] = True
        if "w" not in moneda:
            moneda["w"] = 24
        if "h" not in moneda:
            moneda["h"] = 24
        if "valor" not in moneda:
            moneda["valor"] = VALOR_MONEDA_ORO if moneda.get("subtipo") == "moneda_oro" else VALOR_MONEDA_BRONCE

    for enemigo in mapa_juego["enemigos"]:
        enemigo["canvas_id"] = None
        enemigo["label_id"] = None
        enemigo["activo"] = True

        if enemigo["subtipo"] == "slime_rojo":
            if "vx" not in enemigo:
                enemigo["vx"] = 2.2
            if "vy" not in enemigo:
                enemigo["vy"] = 0
            if "limite_izquierdo" not in enemigo:
                enemigo["limite_izquierdo"] = enemigo["x"] - 90
            if "limite_derecho" not in enemigo:
                enemigo["limite_derecho"] = enemigo["x"] + 140
        elif enemigo["subtipo"] == "bola_fuego":
            if "vx" not in enemigo:
                enemigo["vx"] = 0
            if "vy" not in enemigo:
                enemigo["vy"] = 2.8
            if "limite_superior" not in enemigo:
                enemigo["limite_superior"] = enemigo["y"] - 100
            if "limite_inferior" not in enemigo:
                enemigo["limite_inferior"] = enemigo["y"] + 140
        elif enemigo["subtipo"] == "lanzador":
            if "proyectil" not in enemigo:
                enemigo["proyectil"] = crear_lanzador(enemigo["x"], enemigo["y"])["proyectil"]

            enemigo["proyectil"]["canvas_id"] = None
            enemigo["proyectil"]["activo"] = True

            if "inicio_x" not in enemigo["proyectil"]:
                enemigo["proyectil"]["inicio_x"] = enemigo["x"] - 18
            if "distancia" not in enemigo["proyectil"]:
                enemigo["proyectil"]["distancia"] = 260
            if "vx" not in enemigo["proyectil"]:
                enemigo["proyectil"]["vx"] = -4
            if "vy" not in enemigo["proyectil"]:
                enemigo["proyectil"]["vy"] = 0

    return mapa_juego


def cargar_mapa_creado():
    """Descripcion: carga el ultimo mapa creado guardado en disco.
    Entradas: ninguna.
    Salidas: dict del mapa o None si no existe archivo.
    Restricciones: el JSON debe ser valido.
    """
    if not os.path.exists(RUTA_MAPA_CREADO):
        return None

    with open(RUTA_MAPA_CREADO, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def crear_registro_mapa(nombre, mapa):
    """Descripcion: crea un registro con metadatos para lista de mapas de usuario.
    Entradas: nombre (str), mapa (dict).
    Salidas: dict con nombre, fecha y mapa.
    Restricciones: nombre y mapa deben ser serializables a JSON.
    """
    return {
        "nombre": nombre,
        "fecha": time.strftime("%Y-%m-%d %H:%M:%S"),
        "mapa": mapa,
    }


def cargar_mapas_usuario():
    """Descripcion: carga la coleccion de mapas del usuario desde archivo.
    Entradas: ninguna.
    Salidas: lista de registros de mapas (maximo definido).
    Restricciones: si el contenido no es lista, retorna lista vacia.
    """
    if not os.path.exists(RUTA_MAPAS_USUARIO):
        return []

    with open(RUTA_MAPAS_USUARIO, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    if isinstance(datos, list):
        return datos[:CANTIDAD_MAXIMA_MAPAS]

    return []


def guardar_mapa_usuario(mapa, nombre="Mapa creado"):
    """Descripcion: guarda un mapa de usuario y conserva solo los mas recientes.
    Entradas: mapa (dict), nombre (str opcional).
    Salidas: lista actualizada de mapas guardados.
    Restricciones: mantiene un maximo de CANTIDAD_MAXIMA_MAPAS registros.
    """
    os.makedirs(os.path.dirname(RUTA_MAPAS_USUARIO), exist_ok=True)
    mapas_guardados = cargar_mapas_usuario()
    nuevo_registro = crear_registro_mapa(nombre, mapa)
    mapas_guardados.insert(0, nuevo_registro)
    mapas_guardados = mapas_guardados[:CANTIDAD_MAXIMA_MAPAS]

    with open(RUTA_MAPAS_USUARIO, "w", encoding="utf-8") as archivo:
        json.dump(mapas_guardados, archivo, indent=4, ensure_ascii=False)

    with open(RUTA_MAPA_CREADO, "w", encoding="utf-8") as archivo:
        json.dump(mapa, archivo, indent=4, ensure_ascii=False)

    return mapas_guardados


def obtener_opciones_mapas():
    """Descripcion: genera opciones de seleccion entre mapa base y mapas creados.
    Entradas: ninguna.
    Salidas: lista de dicts con nombre, descripcion y mapa.
    Restricciones: siempre incluye el mapa generico.
    """
    opciones = [
        {
            "nombre": "Mapa genérico",
            "descripcion": "Nivel fijo incluido en el proyecto",
            "mapa": crear_mapa_basico(),
        }
    ]

    mapas_guardados = cargar_mapas_usuario()
    for indice, registro in enumerate(mapas_guardados, start=1):
        nombre = registro.get("nombre", f"Mapa creado {indice}")
        fecha = registro.get("fecha", "sin fecha")
        opciones.append(
            {
                "nombre": f"{nombre} #{indice}",
                "descripcion": f"Creado: {fecha}",
                "mapa": registro["mapa"],
            }
        )

    return opciones
