def actualizar_detalles(canvas, entidad):
    """Descripcion: reposiciona los detalles graficos de una entidad en el canvas.
    Entradas: canvas (tk.Canvas), entidad (dict con x,y y detalles).
    Salidas: ninguna; actualiza coordenadas de elementos secundarios.
    Restricciones: cada detalle debe incluir canvas_id y coordenadas relativas.
    """
    for detalle in entidad.get("detalles", []):
        coordenadas = []

        for indice, valor in enumerate(detalle["coordenadas"]):
            if indice % 2 == 0:
                coordenadas.append(entidad["x"] + valor)
            else:
                coordenadas.append(entidad["y"] + valor)

        canvas.coords(detalle["canvas_id"], *coordenadas)


def mover_enemigos(canvas, mapa):
    """Descripcion: actualiza logica y dibujo de enemigos activos del mapa.
    Entradas: canvas (tk.Canvas), mapa (dict con enemigos).
    Salidas: ninguna; modifica posiciones y coordenadas en pantalla.
    Restricciones: cada subtipo de enemigo debe cumplir estructura esperada.
    """
    for enemigo in mapa["enemigos"]:
        if not enemigo["activo"]:
            continue

        if enemigo["subtipo"] == "slime_rojo":
            enemigo["x"] += enemigo["vx"]

            if enemigo["x"] <= enemigo["limite_izquierdo"]:
                enemigo["x"] = enemigo["limite_izquierdo"]
                enemigo["vx"] = abs(enemigo["vx"])
            elif enemigo["x"] + enemigo["w"] >= enemigo["limite_derecho"]:
                enemigo["x"] = enemigo["limite_derecho"] - enemigo["w"]
                enemigo["vx"] = -abs(enemigo["vx"])

        elif enemigo["subtipo"] == "bola_fuego":
            enemigo["y"] += enemigo["vy"]

            if enemigo["y"] <= enemigo["limite_superior"]:
                enemigo["y"] = enemigo["limite_superior"]
                enemigo["vy"] = abs(enemigo["vy"])
            elif enemigo["y"] + enemigo["h"] >= enemigo["limite_inferior"]:
                enemigo["y"] = enemigo["limite_inferior"] - enemigo["h"]
                enemigo["vy"] = -abs(enemigo["vy"])

        elif enemigo["subtipo"] == "lanzador":
            proyectil = enemigo["proyectil"]
            proyectil["x"] += proyectil["vx"]
            proyectil["y"] += proyectil["vy"]

            if proyectil["x"] <= proyectil["inicio_x"] - proyectil["distancia"]:
                proyectil["x"] = enemigo["x"] - 18
                proyectil["y"] = enemigo["y"] + 15

        canvas.coords(
            enemigo["canvas_id"],
            enemigo["x"],
            enemigo["y"],
            enemigo["x"] + enemigo["w"],
            enemigo["y"] + enemigo["h"],
        )
        canvas.coords(
            enemigo["label_id"],
            enemigo["x"] + enemigo["w"] / 2,
            enemigo["y"] - 14,
        )
        actualizar_detalles(canvas, enemigo)

        if enemigo["subtipo"] == "lanzador":
            proyectil = enemigo["proyectil"]
            canvas.coords(
                proyectil["canvas_id"],
                proyectil["x"],
                proyectil["y"],
                proyectil["x"] + proyectil["w"],
                proyectil["y"] + proyectil["h"],
            )
