#=================================================================#
# punto destinatario del jugador
#=================================================================#

def crear_meta(x, y):
    meta = {
        "id": "meta1",
        "nombre": "meta",
        "tipo": "fijo",
        "subtipo": "meta",

        "x": x,
        "y": y,

        "radio": 30,

        "activo": True,
        "visible": True,

        "hitbox": None
    }
    return meta