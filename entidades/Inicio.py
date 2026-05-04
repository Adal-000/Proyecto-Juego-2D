#=================================================================#
# punto de inicio del jugador
#=================================================================#

def crear_inicio(x, y):
    inicio = {
        "id": "inicio1",
        "nombre": "inicio",
        "tipo": "fijo",
        "subtipo": "inicio",

        "x": x,
        "y": y,

        "radio": 30,

        "activo": True,
        "visible": True,

        "hitbox": None
    }
    return inicio