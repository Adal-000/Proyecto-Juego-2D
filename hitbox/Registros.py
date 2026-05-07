def crear_registro_hitbox():
    registro = {
        "jugador": None,
        "inicio": None,
        "meta": None,

        "monedas": [],
        "enemigos": [],
        "trampas": [],
        "plataformas": [],
        "conductos": []
    }

    return registro


def obtener_grupo_por_tipo(tipo):
    if tipo == "jugador":
        return "jugador"

    elif tipo == "inicio":
        return "inicio"

    elif tipo == "meta":
        return "meta"

    elif tipo == "moneda":
        return "monedas"

    elif tipo == "enemigo":
        return "enemigos"

    elif tipo == "trampa":
        return "trampas"

    elif tipo == "plataforma":
        return "plataformas"

    elif tipo == "conducto":
        return "conductos"

    else:
        return None
    

def registrar_hitbox(registro, objeto):
    grupo = obtener_grupo_por_tipo(objeto["tipo"])

    if grupo == None:
        return registro

    if objeto["hitbox"] == None:
        return registro

    if grupo == "jugador" or grupo == "inicio" or grupo == "meta":
        registro[grupo] = objeto["hitbox"]

    else:
        registro[grupo].append(objeto["hitbox"])

    return registro