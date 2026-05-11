# Citaciones y Atribuciones

## Codigo del Proyecto
El codigo de este proyecto es **original** y fue desarrollado especificamente para este juego de plataformas.
No se extrajo codigo completo de sitios externos ni repositorios públicos.

## Librerias y Modulos Utilizados
Este proyecto usa unicamente modulos incluidos en la distribucion estandar de Python.
No requiere instalacion de paquetes externos via pip.

### Modulos de Python utilizados:
- **tkinter**: Interfaz grafica de escritorio (GUI)
  - Incluido en Python estandar
  - Documentacion: https://docs.python.org/3/library/tkinter.html
  - Uso en proyecto: Todas las ventanas y controles visuales

- **json**: Manejo de formato JSON
  - Incluido en Python estandar
  - Documentacion: https://docs.python.org/3/library/json.html
  - Uso en proyecto: Lectura/escritura de configuracion y mapas

- **os**: Operaciones con sistema operativo y rutas
  - Incluido en Python estandar
  - Documentacion: https://docs.python.org/3/library/os.html
  - Uso en proyecto: Manejo de rutas de archivos

- **sys**: Variables y funciones especificas del sistema
  - Incluido en Python estandar
  - Documentacion: https://docs.python.org/3/library/sys.html
  - Uso en proyecto: Manipulacion de sys.path para imports relativos

- **time**: Funciones relacionadas con tiempo
  - Incluido en Python estandar
  - Documentacion: https://docs.python.org/3/library/time.html
  - Uso en proyecto: Timestamp de mapas, calculo de puntaje segun tiempo

- **copy**: Crear copias profundas de objetos
  - Incluido en Python estandar
  - Documentacion: https://docs.python.org/3/library/copy.html
  - Uso en proyecto: copy.deepcopy para mapas

- **math**: Funciones matematicas
  - Incluido en Python estandar
  - Documentacion: https://docs.python.org/3/library/math.html
  - Uso en proyecto: Calculo de ondas sinusoidales en generacion de audio

- **struct**: Empaquetar y desempaquetar datos binarios
  - Incluido en Python estandar
  - Documentacion: https://docs.python.org/3/library/struct.html
  - Uso en proyecto: Conversion de muestras de audio a formato WAV

- **wave**: Lectura y escritura de archivos WAV
  - Incluido en Python estandar
  - Documentacion: https://docs.python.org/3/library/wave.html
  - Uso en proyecto: Generacion de archivos WAV para musica

- **importlib**: Importacion dinamica de modulos
  - Incluido en Python estandar
  - Documentacion: https://docs.python.org/3/library/importlib.html
  - Uso en proyecto: Deteccion dinamica de modulo winsound

- **collections**: Estructuras de datos especializadas
  - Incluido en Python estandar
  - Documentacion: https://docs.python.org/3/library/collections.html
  - Uso en proyecto: deque para BFS en validacion de camino

- **winsound**: Reproduccion de sonido (solo Windows)
  - Incluido en Python para Windows
  - Documentacion: https://docs.python.org/3/library/winsound.html
  - Uso en proyecto: Reproduccion de archivos WAV con opciones avanzadas

## Patrones y Conceptos Tomados de Fuentes Publicas
### 1) Deteccion de Colisiones AABBs (Axis-Aligned Bounding Box)
El algoritmo de colision usado en jugabilidad/Colisiones.py sigue el patrón estandar AABB,
que es un concepto ampliamente documentado en teoria de videojuegos.

Referencia general:
- Concept: AABB Collision Detection
- Documentacion: https://en.wikipedia.org/wiki/Collision_detection#Axis-aligned_bounding_boxes
- Aplicacion en proyecto: Deteccion simple y eficiente entre rectangulos

### 2) Pathfinding con BFS (Breadth-First Search)
El algoritmo de validacion de camino usa BFS para encontrar si existe ruta desde inicio a meta.
BFS es un algoritmo clasico en teoria de grafos.

Referencia:
- Algoritmo: BFS (Breadth-First Search)
- Documentacion: https://en.wikipedia.org/wiki/Breadth-first_search
- Aplicacion en proyecto: mapas/Validacion.py, funcion validar_alcance_meta

### 3) Generacion de Audio Sintetico
La generacion de notas musicales en jugabilidad/Musica.py utiliza:
- Funcion seno para onda fundamental
- Armonico suave para timbre
- Envolvente ADSR simplificada para envejecimiento

Concepto general (sintesis aditiva):
- Documentacion: https://en.wikipedia.org/wiki/Additive_synthesis
- Referencia practica: Sintesis estandar en DSP (Digital Signal Processing)

## Herramientas y Tecnologia
- **Lenguaje**: Python 3.10+
  - Web: https://www.python.org/
  - Licencia: PSF License

- **Editor recomendado**: Visual Studio Code
  - Web: https://code.visualstudio.com/
  - Licencia: MIT

## Inspiracion del Proyecto
Este juego se inspiro en:
- Juegos clasicos de plataformas 2D (estilo Donkey Kong, Super Mario)
- Mecanicas simples pero jugables
- Concepto de editor integrado para crear niveles personalizados

## Licencia del Proyecto
Define aqui la licencia que deseas usar (MIT, GPL, CC BY, etc).
Si quieres distribuir publicamente, considera usar:
- MIT License: Permisiva, libre para uso comercial
- GNU GPL: Requiere que derivados sean también de fuente abierta
- Creative Commons: Si deseas flexibilidad en atribuciones

## Cambios y Mejoras Futuras
Si en futuro se incorporan dependencias externas (por ejemplo pygame, numpy),
se actualizara este archivo con las citaciones correspondientes.

## Resumen
Este es un proyecto educativo/academico con codigo original que utiliza
unicamente herramientas y librerias estandar de Python.
No contiene codigo copiado de repositorios públicos sin atribuccion.
