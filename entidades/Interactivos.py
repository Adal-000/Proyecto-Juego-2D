#=================================================================#
# interactivos donde el jugador tiene a uso
#=================================================================#


def crear_baba(x, y):
    baba = {
        "nombre": "Baba",
        "tipo": "interactivo",
        "subtipo": "facilitador",

        "x": x,
        "y": y,
        "radio": 30,

        "activo": True,
        "visible": True,

        "hitbox": None
    }

    return baba


def crear_conducto_baba(x, y, cantidad, separacion=30):
    conducto = []

    for i in range(cantidad):
        baba = crear_baba(
            x,
            y + i * separacion
        )

        conducto.append(baba)

    return conducto