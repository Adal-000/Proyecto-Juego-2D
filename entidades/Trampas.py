#=================================================================#
# trampas perdida de vida
#=================================================================#

def crear_pinchos(x, y):
    pinchos = {
        "id": "pinchos1",
        "nombre": "Pinchos",
        "tipo": "trampa",
        "subtipo": "pinchos",

        "x": x,
        "y": y,
        "radio": 30,

        "dano": 1,

        "activo": True,
        "visible": True,

        "hitbox": None
    }

    return pinchos


def crear_lava(x, y):
    lava = {
        "id": "lava1",
        "nombre": "Lava",
        "tipo": "trampa",
        "subtipo": "lava",

        "x": x,
        "y": y,
        "radio": 30,

        "dano": 1,

        "activo": True,
        "visible": True,

        "hitbox": None
    }

    return lava