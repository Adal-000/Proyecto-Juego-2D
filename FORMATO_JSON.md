# Formato JSON en el proyecto

## Objetivo de este documento
Este archivo explica:
1. Que estructuras JSON usa el proyecto.
2. Como se leen y escriben esos archivos.
3. Como editar JSON sin romper el juego.
4. Como se aplico JSON en el flujo real del proyecto.

## Que es JSON
JSON es un formato de texto para guardar datos estructurados.
En este proyecto se usa para persistir configuracion y mapas entre ejecuciones.

Reglas basicas:
- Usa llaves para objetos: { }
- Usa corchetes para listas: [ ]
- Las claves van entre comillas dobles
- Los valores pueden ser texto, numero, true, false, null, objeto o lista
- No se permiten comentarios dentro de JSON

## Archivos JSON que usa el proyecto
- Interfaz/configuracion.json
- mapas/mapa_creado.json
- mapas/mapas_creados.json

## 1) Configuracion de musica
Archivo: Interfaz/configuracion.json

Estructura minima esperada:
    {
      "musica_activa": true,
      "cancion": "aventura"
    }

Significado de campos:
- musica_activa: true o false
- cancion: clave de cancion soportada (aventura, rapida, tranquila, retro_winsound)

Compatibilidad incluida en el codigo:
- Si aparece retro_pygame, el sistema lo convierte a retro_winsound para mantener compatibilidad.
- Si la cancion no existe, se usa el valor por defecto.

Donde se maneja:
- Lectura y normalizacion: Interfaz/Settings.py, funcion cargar_configuracion
- Guardado: Interfaz/Settings.py, funcion guardar_configuracion
- Conversion a config final de juego: Interfaz/Settings.py, funcion obtener_configuracion_musica

## 2) Ultimo mapa creado
Archivo: mapas/mapa_creado.json

Este archivo guarda un solo mapa jugable.

Estructura general:
    {
      "inicio": {"x": 0, "y": 520},
      "meta": {"x": 440, "y": 440, "w": 45, "h": 75},
      "plataformas": [ ... ],
      "escaleras": [ ... ],
      "enemigos": [ ... ],
      "trampas": [ ... ],
      "monedas": [ ... ],
      "puntaje_mapa": 20
    }

Notas importantes:
- inicio y meta son obligatorios para que el mapa sea jugable.
- plataformas, escaleras, enemigos, trampas y monedas son listas.
- puntaje_mapa es un entero calculado por el editor.

Donde se maneja:
- Guardado del mapa: mapas/Mapa.py, funcion guardar_mapa_usuario
- Carga del ultimo mapa: mapas/Mapa.py, funcion cargar_mapa_creado
- Normalizacion antes de jugar: mapas/Mapa.py, funcion preparar_mapa_para_jugar

## 3) Historial de mapas creados
Archivo: mapas/mapas_creados.json

Guarda una lista de registros con metadatos.

Estructura:
    [
      {
        "nombre": "Mapa creado",
        "fecha": "2026-05-08 00:32:27",
        "mapa": { ... objeto de mapa jugable ... }
      }
    ]

Reglas aplicadas por el proyecto:
- Solo se conservan los ultimos 3 mapas.
- El mapa mas nuevo se inserta al inicio de la lista.

Donde se maneja:
- Lectura: mapas/Mapa.py, funcion cargar_mapas_usuario
- Escritura y recorte maximo: mapas/Mapa.py, funcion guardar_mapa_usuario
- Creacion de registro con fecha: mapas/Mapa.py, funcion crear_registro_mapa

## Como se usa JSON dentro del flujo del proyecto
1. El usuario crea un mapa en el editor.
2. El editor valida estructura y camino posible.
3. El mapa del editor se convierte a formato jugable.
4. Se guarda en dos JSON:
   - mapas/mapa_creado.json (ultimo mapa)
   - mapas/mapas_creados.json (historial limitado)
5. Al jugar, se carga mapa base o mapa JSON de usuario.
6. Antes de iniciar partida, se normalizan campos faltantes para evitar fallos.

## Diferencia entre formato de editor y formato jugable
El editor trabaja con celdas (fila, columna).
El juego trabaja con coordenadas reales (x, y, w, h).

Transformacion clave:
- Editor: {"fila": 12, "columna": 3}
- Juego: {"x": 120, "y": 480, "w": 40, "h": 40}

Esta conversion se realiza en:
- mapas/Validacion.py, funcion convertir_a_mapa_juego

## Buenas practicas para editar JSON manualmente
- Haz copia de seguridad antes de editar.
- Mantener comillas dobles en todas las claves y textos.
- No agregar comentarios dentro del JSON.
- Revisar comas finales: en JSON no se permiten comas sobrantes.
- Mantener tipos correctos:
  - true/false para booleanos
  - numeros sin comillas para coordenadas y puntaje
  - texto con comillas para nombres y claves

## Errores comunes
- Usar comillas simples en vez de dobles.
- Dejar una coma extra al final del ultimo campo.
- Borrar claves requeridas como inicio o meta.
- Cambiar nombres de claves esperadas por el codigo.

## Ejemplo rapido valido de configuracion
    {
      "musica_activa": false,
      "cancion": "tranquila"
    }

## Ejemplo rapido valido de registro de mapa
    {
      "nombre": "Mi mapa 1",
      "fecha": "2026-05-08 12:30:00",
      "mapa": {
        "inicio": {"x": 80, "y": 520},
        "meta": {"x": 1000, "y": 200, "w": 45, "h": 75},
        "plataformas": [],
        "escaleras": [],
        "enemigos": [],
        "trampas": [],
        "monedas": [],
        "puntaje_mapa": 0
      }
    }

## Resumen
En este proyecto JSON se uso para persistencia simple, legible y facil de mantener:
- Configuracion del juego.
- Almacenamiento de mapas creados.
- Intercambio entre editor y modo de juego mediante una estructura consistente.
