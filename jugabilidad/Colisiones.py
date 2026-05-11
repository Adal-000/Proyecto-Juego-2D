def rectangulos_colisionan(a, b):
    """Descripcion: determina si dos rectangulos se superponen.
    Entradas: a (dict con x,y,w,h), b (dict con x,y,w,h).
    Salidas: bool indicando si existe colision.
    Restricciones: ambos rectangulos deben contener las cuatro claves numericas.
    """
    return (
        a["x"] < b["x"] + b["w"]
        and a["x"] + a["w"] > b["x"]
        and a["y"] < b["y"] + b["h"]
        and a["y"] + a["h"] > b["y"]
    )


def revisar_colision_enemigos(jugador, mapa):
    """Descripcion: verifica choque del jugador con enemigos o proyectiles.
    Entradas: jugador (dict), mapa (dict con lista de enemigos).
    Salidas: bool; True si hay colision peligrosa.
    Restricciones: cada enemigo debe incluir subtipo y estado activo.
    """
    for enemigo in mapa["enemigos"]:
        if enemigo["activo"] and rectangulos_colisionan(jugador, enemigo):
            return True

        if enemigo["activo"] and enemigo["subtipo"] == "lanzador":
            proyectil = enemigo["proyectil"]
            if proyectil["activo"] and rectangulos_colisionan(jugador, proyectil):
                return True

    return False


def revisar_colision_trampas(jugador, mapa):
    """Descripcion: verifica choque del jugador con trampas del mapa.
    Entradas: jugador (dict), mapa (dict con lista de trampas).
    Salidas: bool; True si toca una trampa.
    Restricciones: cada trampa debe tener estructura de rectangulo valida.
    """
    for trampa in mapa["trampas"]:
        if rectangulos_colisionan(jugador, trampa):
            return True

    return False
