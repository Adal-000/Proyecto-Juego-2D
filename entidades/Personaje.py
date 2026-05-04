#=================================================================#
# Jugador un slime
#=================================================================#

def crear_personaje(x, y):
    personaje = {
        "id": "jugador1",
        "nombre": "Slime",
        "tipo": "jugador",
        "subtipo": "slime",

        "x": x,
        "y": y,

        "radio": 30,
        "radio_normal": 30,
        "radio_shift": 15,

        "vx": 0,
        "vy": 0,

        "vidas": 3,
        "puntos": 0,

        "estado": "normal",
        "suelo": False,
        "conducto": False,

        "hitbox": None
    }
    return personaje
    