import os
import time

from mapas.Mapa import ALTO_JUGADOR, ANCHO_JUGADOR

RUTA_PUNTAJES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "puntajes.txt")


def crear_jugador(inicio):
    """Descripcion: crea el estado inicial del jugador para una partida.
    Entradas: inicio (dict con x e y).
    Salidas: dict con posicion, tamano y estado de movimiento del jugador.
    Restricciones: inicio debe incluir coordenadas numericas validas.
    """
    return {
        "x": inicio["x"],
        "y": inicio["y"],
        "w": ANCHO_JUGADOR,
        "h": ALTO_JUGADOR,
        "vx": 0,
        "vy": 0,
        "en_suelo": True,
        "en_escalera": False,
    }


def cargar_mejores_puntajes():
    """Descripcion: lee y ordena los mejores puntajes guardados.
    Entradas: ninguna.
    Salidas: lista de tuplas (nombre, puntaje), maximo 5 elementos.
    Restricciones: solo considera lineas con formato nombre,puntaje entero.
    """
    registros = []

    if os.path.exists(RUTA_PUNTAJES):
        with open(RUTA_PUNTAJES, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                partes = linea.strip().split(",", 1)
                if len(partes) == 2 and partes[1].isdigit():
                    registros.append((partes[0], int(partes[1])))

    registros.sort(key=lambda dato: dato[1], reverse=True)
    return registros[:5]


def guardar_puntaje(nombre, puntos):
    """Descripcion: agrega un puntaje y conserva solo el top 5.
    Entradas: nombre (str), puntos (int).
    Salidas: ninguna; sobrescribe el archivo de puntajes.
    Restricciones: puntos debe ser entero para mantener consistencia del ranking.
    """
    registros = cargar_mejores_puntajes()
    registros.append((nombre, puntos))
    registros.sort(key=lambda dato: dato[1], reverse=True)
    registros = registros[:5]

    with open(RUTA_PUNTAJES, "w", encoding="utf-8") as archivo:
        for jugador, puntaje in registros:
            archivo.write(f"{jugador},{puntaje}\n")


def calcular_puntaje(inicio_tiempo, puntaje_mapa=0, puntaje_extra=0):
    """Descripcion: calcula el puntaje final segun tiempo y bonificaciones.
    Entradas: inicio_tiempo (timestamp), puntaje_mapa (int), puntaje_extra (int).
    Salidas: int con puntaje final.
    Restricciones: aplica un minimo de 100 puntos.
    """
    segundos = int(time.time() - inicio_tiempo)
    puntos = 1000 + puntaje_mapa + puntaje_extra - segundos * 10

    if puntos < 100:
        puntos = 100

    return puntos
