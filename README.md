# JuegoPython - Juego de plataformas con editor de mapas

## Descripcion
Este proyecto es un juego de plataformas hecho en Python con interfaz grafica en Tkinter.
Incluye:
- Menu principal.
- Modo de juego con colisiones, enemigos, trampas y monedas.
- Editor visual de mapas.
- Validacion de mapas (inicio, meta y camino alcanzable).
- Guardado de mapas creados por el usuario.
- Sistema de puntajes.
- Configuracion de musica.

## Objetivo del juego
El jugador debe llegar desde el punto de inicio hasta la meta evitando enemigos y trampas, y puede recoger monedas para aumentar el puntaje final.

## Caracteristicas principales
- Juego 2D en tiempo real con movimiento horizontal, salto y escaleras.
- Enemigos con comportamientos distintos:
  - Slime rojo (patrulla horizontal).
  - Bola de fuego (movimiento vertical).
  - Lanzador con proyectil.
- Editor de mapas por celdas con herramientas para:
  - Inicio.
  - Meta.
  - Bloques.
  - Escaleras.
  - Enemigos.
  - Trampas.
  - Monedas de bronce y oro.
- Validacion automatica del mapa antes de guardar.
- Persistencia de mapas y top de puntajes.

## Estructura del proyecto
- [Interfaz/Main.py](Interfaz/Main.py): entrada principal y menu.
- [Interfaz/Jugar.py](Interfaz/Jugar.py): ciclo de juego, dibujo, controles y UI de partida.
- [Interfaz/Editor.py](Interfaz/Editor.py): interfaz del editor de mapas.
- [Interfaz/Puntajes.py](Interfaz/Puntajes.py): pantalla de mejores puntajes.
- [Interfaz/Settings.py](Interfaz/Settings.py): configuracion de musica.
- [jugabilidad/Estado.py](jugabilidad/Estado.py): estado del jugador y calculo/guardado de puntajes.
- [jugabilidad/Colisiones.py](jugabilidad/Colisiones.py): deteccion de colisiones.
- [jugabilidad/Movimientos.py](jugabilidad/Movimientos.py): movimiento de enemigos y actualizacion grafica.
- [jugabilidad/Musica.py](jugabilidad/Musica.py): reproduccion y generacion de audio (beep/winsound).
- [mapas/Mapa.py](mapas/Mapa.py): mapa base, creacion de entidades y guardado/carga de mapas.
- [mapas/Validacion.py](mapas/Validacion.py): reglas del editor, conversion y validacion de camino.
- [mapas/Editor.py](mapas/Editor.py): apoyo visual para dibujado del editor.
- [puntajes.txt](puntajes.txt): almacenamiento de mejores puntajes.

## Requisitos
- Python 3.10 o superior.
- Tkinter disponible (normalmente incluido en Python estandar).
- Sistema Windows recomendado para backend winsound.

## Como ejecutar
Desde la raiz del proyecto, ejecuta:

```powershell
python Interfaz/Main.py
```

Si tu instalacion usa una ruta especifica de Python:

```powershell
& c:\python314\python.exe Interfaz/Main.py
```

## Controles del juego
- Flecha izquierda: mover a la izquierda.
- Flecha derecha: mover a la derecha.
- Espacio: saltar.
- Flecha arriba / abajo: subir o bajar escaleras.

## Flujo de uso recomendado
1. Abre el menu principal.
2. Entra a Jugar para seleccionar mapa y comenzar partida.
3. Entra a Editor para crear mapas personalizados.
4. Usa Validar camino antes de guardar en el editor.
5. Guarda el mapa y luego juega ese mapa.
6. Revisa los mejores puntajes en la seccion Puntajes.
7. Ajusta musica en Settings.

## Sistema de mapas
- Siempre existe un mapa generico disponible.
- Los mapas del usuario se guardan en:
  - [mapas/mapas_creados.json](mapas/mapas_creados.json)
  - [mapas/mapa_creado.json](mapas/mapa_creado.json)
- Se conservan los ultimos 3 mapas creados.

## Sistema de puntajes
- El puntaje considera tiempo, puntaje base del mapa y monedas recolectadas.
- Se almacena un top de 5 puntajes en [puntajes.txt](puntajes.txt).

## Musica
- La configuracion se guarda en [Interfaz/configuracion.json](Interfaz/configuracion.json).
- Soporta modo activo/silenciado y seleccion de cancion.
- Puede usar winsound (Windows) para reproducir WAV generado automaticamente.

## Problemas comunes
- Error de modulo al ejecutar un archivo suelto:
  - Ejecuta siempre desde la raiz del proyecto.
- No se puede guardar un mapa:
  - Verifica que tenga inicio, meta y camino valido.
- No se escucha musica:
  - Revisa si esta silenciada en Settings.
  - En backend winsound, usa Windows.

## Proximas mejoras sugeridas
- Agregar pruebas automaticas para logica de colisiones y validacion.
- Incluir selector de dificultad.
- Mostrar nombre editable para guardar puntaje del jugador.
- Exportar/importar mapas en archivos independientes.

## Licencia
Proyecto academico/educativo. Ajusta esta seccion segun la licencia que desees usar (por ejemplo, MIT).
