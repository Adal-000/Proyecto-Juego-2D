#=================================================================#
# enemigos reducen vidas
#=================================================================#


def crear_slime_rojo(x, y):
    slime_rojo = {
        "nombre": "Slime Rojo",
        "tipo": "enemigo",
        "subtipo": "slime_rojo",

        "x": x,
        "y": y,
        "radio": 30,

        "vx": 2,
        "vy": 0,
        "direccion": 1,

        "limite_izquierdo": x - 100,
        "limite_derecho": x + 100,

        "activo": True,
        "visible": True,

        "hitbox": None
    }

    return slime_rojo


def crear_bola_fuego(x, y):
    bola_fuego = {
        "nombre": "Bola de Fuego",
        "tipo": "enemigo",
        "subtipo": "bola_fuego",

        "x": x,
        "y": y,
        "radio": 30,

        "vx": 2,
        "vy": 0,
        "direccion": 1,

        "limite_superior": y - 100,
        "limite_inferior": y + 100,

        "activo": True,
        "visible": True,

        "hitbox": None
    }

    return bola_fuego