#=================================================================#
# hitboxes de diiversas entidades
#=================================================================#


def obtener_radio_hitbox(subtipo):
    radios = {
        "slime": 30,
        "moneda": 15,
        "inicio": 30,
        "meta": 30,

        "pinchos": 30,
        "lava": 30,

        "slime_rojo": 30,
        "bola_fuego": 30,

        "plataforma_roca": 30,
        "suelo": 30,

        "facilitador": 30
    }

    if subtipo in radios:
        return radios[subtipo]
    else:
        return 30