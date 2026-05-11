import importlib
import importlib.util
import math
import os
import struct
import wave

RUTA_MUSICA_GENERADA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Interfaz", "musica_generada")
VOLUMEN = 0.28
FRECUENCIA_MUESTREO = 44100


def winsound_disponible():
    """Descripcion: comprueba si el modulo winsound esta disponible en el entorno.
    Entradas: ninguna.
    Salidas: bool.
    Restricciones: pensado para plataformas que soporten winsound (Windows).
    """
    return importlib.util.find_spec("winsound") is not None


def limitar_muestra(valor):
    """Descripcion: limita una muestra de audio al rango valido de 16 bits.
    Entradas: valor (float o int).
    Salidas: int en el rango [-32768, 32767].
    Restricciones: se usa para escritura PCM de 16 bits.
    """
    if valor > 32767:
        return 32767
    if valor < -32768:
        return -32768
    return int(valor)


def crear_muestras_nota(frecuencia, duracion_ms):
    """Descripcion: genera muestras PCM para una nota con envolvente simple.
    Entradas: frecuencia (float), duracion_ms (int).
    Salidas: lista de enteros PCM.
    Restricciones: duracion_ms debe ser positiva y frecuencia mayor a 0 para tono audible.
    """
    cantidad_muestras = int(FRECUENCIA_MUESTREO * duracion_ms / 1000)
    muestras = []

    for indice in range(cantidad_muestras):
        tiempo = indice / FRECUENCIA_MUESTREO
        onda_principal = math.sin(2 * math.pi * frecuencia * tiempo)
        armonico_suave = 0.35 * math.sin(2 * math.pi * frecuencia * 2 * tiempo)
        envolvente = 1.0

        if indice < 800:
            envolvente = indice / 800
        elif indice > cantidad_muestras - 1600:
            envolvente = max(0, (cantidad_muestras - indice) / 1600)

        muestra = (onda_principal + armonico_suave) * 32767 * VOLUMEN * envolvente
        muestras.append(limitar_muestra(muestra))

    return muestras


def crear_archivo_wav(nombre_archivo, notas):
    """Descripcion: crea un archivo WAV a partir de una secuencia de notas.
    Entradas: nombre_archivo (str), notas (lista de pares frecuencia,duracion).
    Salidas: ruta absoluta del WAV generado o existente.
    Restricciones: notas debe contener pares numericos validos.
    """
    os.makedirs(RUTA_MUSICA_GENERADA, exist_ok=True)
    ruta_archivo = os.path.join(RUTA_MUSICA_GENERADA, nombre_archivo)

    if os.path.exists(ruta_archivo):
        return ruta_archivo

    with wave.open(ruta_archivo, "w") as archivo:
        archivo.setnchannels(1)
        archivo.setsampwidth(2)
        archivo.setframerate(FRECUENCIA_MUESTREO)

        for frecuencia, duracion_ms in notas:
            if frecuencia <= 0:
                muestras = [0] * int(FRECUENCIA_MUESTREO * duracion_ms / 1000)
            else:
                muestras = crear_muestras_nota(frecuencia, duracion_ms)

            for muestra in muestras:
                archivo.writeframes(struct.pack("<h", muestra))

    return ruta_archivo


def cargar_winsound():
    """Descripcion: importa winsound si esta disponible.
    Entradas: ninguna.
    Salidas: modulo winsound o None.
    Restricciones: requiere soporte del sistema operativo.
    """
    if not winsound_disponible():
        return None

    return importlib.import_module("winsound")


def iniciar_musica_winsound(configuracion_musica):
    """Descripcion: inicia reproduccion en bucle con winsound segun configuracion.
    Entradas: configuracion_musica (dict con backend, activa, archivo y notas).
    Salidas: bool indicando si se inicio correctamente.
    Restricciones: backend debe ser winsound y la musica debe estar activa.
    """
    if configuracion_musica.get("backend") != "winsound" or not configuracion_musica.get("activa"):
        return False

    winsound = cargar_winsound()
    if winsound is None:
        return False

    try:
        ruta_archivo = crear_archivo_wav(
            configuracion_musica["archivo"],
            configuracion_musica["notas"],
        )
        winsound.PlaySound(
            ruta_archivo,
            winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP,
        )
        return True
    except Exception:
        return False


def detener_musica_winsound():
    """Descripcion: detiene la reproduccion actual iniciada con winsound.
    Entradas: ninguna.
    Salidas: ninguna.
    Restricciones: si winsound no esta disponible, no realiza accion.
    """
    winsound = cargar_winsound()
    if winsound is None:
        return

    try:
        winsound.PlaySound(None, 0)
    except Exception:
        return
