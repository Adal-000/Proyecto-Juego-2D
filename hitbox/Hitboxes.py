from Vocabulario import obtener_radio_hitbox


#=================================================================#
# crea los hitboxes de las entidades
#=================================================================#


def crear_hitbox(objeto):   #Crea una hitbox circular usando los datos de una entidad
    if "radio" in objeto:
        radio = objeto["radio"]
    else:
        radio = obtener_radio_hitbox(objeto["subtipo"])

    hitbox = {
        "tipo": objeto["tipo"],
        "subtipo": objeto["subtipo"],

        "x": objeto["x"],
        "y": objeto["y"],
        "radio": radio,

        "activo": objeto["activo"]
    }

    return hitbox


def asignar_hitbox(objeto):   # Crea una hitbox y la guarda dentro del objeto
    objeto["hitbox"] = crear_hitbox(objeto)

    return objeto


def actualizar_hitbox(objeto):    #Actualiza la hitbox con la posición actual del objeto sirve cuando el jugador o enemigo se mueve
    if objeto["hitbox"] != None:
        objeto["hitbox"]["x"] = objeto["x"]
        objeto["hitbox"]["y"] = objeto["y"]
        objeto["hitbox"]["radio"] = objeto["radio"]
        objeto["hitbox"]["activo"] = objeto["activo"]

    return objeto


def calcular_distancia(hitbox1, hitbox2):  #sistema de colisiones mediante pitagoras
    diferencia_x = hitbox2["x"] - hitbox1["x"]
    diferencia_y = hitbox2["y"] - hitbox1["y"]

    distancia = (diferencia_x ** 2 + diferencia_y ** 2) ** 0.5

    return distancia


def hay_colision(hitbox1, hitbox2):  #Determina si hay colision entre dos hitboxes circulares
    if hitbox1["activo"] == False:
        return False

    if hitbox2["activo"] == False:
        return False

    distancia = calcular_distancia(hitbox1, hitbox2)

    suma_radios = hitbox1["radio"] + hitbox2["radio"]

    if distancia <= suma_radios:
        return True
    else:
        return False