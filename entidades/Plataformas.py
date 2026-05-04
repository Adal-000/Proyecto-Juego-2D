#=================================================================#
# plataforma como solidos
#=================================================================#

def crear_piedra(x, y):
    piedra = {
        "nombre": "Piedra",
        "tipo": "plataforma",
        "subtipo": "plataforma_roca",

        "x": x,
        "y": y,
        "radio": 15,

        "activo": True,
        "visible": True,

        "hitbox": None
    }

    return piedra


def crear_plataforma_roca(x, y, cantidad, separacion=15):
    plataforma = []

    for i in range(cantidad):
        piedra = crear_piedra(
            x + i * separacion,
            y,
            "plataforma_roca"
        )

        plataforma.append(piedra)

    return plataforma


def crear_suelo(x, y, cantidad, separacion=15):
    suelo = []

    for i in range(cantidad):
        piedra = crear_piedra(
            x + i * separacion,
            y,
            "suelo"
        )

        suelo.append(piedra)

    return suelo