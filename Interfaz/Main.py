import tkinter as tk
from Editor import editor
from Jugar import jugar
from Puntajes import mostrar_puntajes
from Settings import settings

ANCHO = 1150
ALTO = 700


def crear_texto(texto, tamano=20, tipo_fuente="Arial Rounded MT Bold", color="black"):
    """
    Descripción:
        Crea un diccionario con las propiedades básicas de texto para usar
        en widgets de Tkinter, como Label o Button.

    Entradas:
        texto: texto que se mostrará en el widget.
        tamano: tamaño de la fuente.
        tipo_fuente: nombre de la fuente que se desea utilizar.
        color: color del texto.

    Salidas:
        Retorna un diccionario con las propiedades:
        text, font y fg.

    Restricciones:
        La fuente solo se usa si está dentro de la lista de fuentes disponibles.
        Si no está disponible, se usa Arial como fuente por defecto.
    """
    fuente_default = "Arial"
    fuentes_disponibles = [
        "Arial",
        "Segoe Script",
        "Gabriola",
        "Comic Sans MS",
        "MV Boli",
        "Lucida Handwriting",
        "Monotype Corsiva",
        "Verdana",
        "Georgia",
        "Cambria",
    ]

    if tipo_fuente in fuentes_disponibles:
        fuente_final = tipo_fuente
    else:
        fuente_final = fuente_default

    return {
        "text": texto,
        "font": (fuente_final, tamano, "bold"),
        "fg": color,
    }


def centrar_ventana(ventana, ancho=ANCHO, alto=ALTO):
    """
    Descripción:
        Centra una ventana de Tkinter en la pantalla del usuario.

    Entradas:
        ventana: ventana de Tkinter que se desea centrar.
        ancho: ancho de la ventana.
        alto: alto de la ventana.

    Salidas:
        No retorna ningún valor.
        Modifica la posición y tamaño de la ventana recibida.

    Restricciones:
        La entrada ventana debe ser un objeto válido de Tkinter.
        El ancho y el alto deben ser valores numéricos enteros positivos.
    """
    p_ancho = ventana.winfo_screenwidth()
    p_alto = ventana.winfo_screenheight()
    x = (p_ancho - ancho) // 2
    y = (p_alto - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


def main():
    """
    Descripción:
        Crea y muestra el menú principal del juego.
        Desde esta ventana se puede acceder al juego, editor, ajustes,
        puntajes o salir del programa.

    Entradas:
        No recibe entradas.

    Salidas:
        No retorna ningún valor.
        Ejecuta la ventana principal del programa.

    Restricciones:
        Los módulos Editor, Jugar, Puntajes y Settings deben existir.
        Las funciones editor, jugar, mostrar_puntajes y settings deben estar
        correctamente definidas en sus respectivos archivos.
    """
    window1 = tk.Tk()
    centrar_ventana(window1)
    window1.title("Main Menu")
    window1.resizable(False, False)
    window1.configure(bg="black")

    def abrir_juego():
        """
        Descripción:
            Abre la ventana o sección del juego.

        Entradas:
            No recibe entradas directas.

        Salidas:
            No retorna ningún valor.
            Llama a la función jugar.

        Restricciones:
            La función jugar debe aceptar como entrada la ventana principal.
        """
        jugar(window1)

    def abrir_editor():
        """
        Descripción:
            Abre la ventana o sección del editor.

        Entradas:
            No recibe entradas directas.

        Salidas:
            No retorna ningún valor.
            Llama a la función editor.

        Restricciones:
            La función editor debe aceptar como entrada la ventana principal.
        """
        editor(window1)

    def abrir_settings():
        """
        Descripción:
            Abre la ventana o sección de configuración.

        Entradas:
            No recibe entradas directas.

        Salidas:
            No retorna ningún valor.
            Llama a la función settings.

        Restricciones:
            La función settings debe aceptar como entrada la ventana principal.
        """
        settings(window1)

    def abrir_puntajes():
        """
        Descripción:
            Abre la ventana o sección donde se muestran los puntajes.

        Entradas:
            No recibe entradas directas.

        Salidas:
            No retorna ningún valor.
            Llama a la función mostrar_puntajes.

        Restricciones:
            La función mostrar_puntajes debe aceptar como entrada la ventana principal.
        """
        mostrar_puntajes(window1)

    title = tk.Label(window1, crear_texto("Juego de Plataformas", 30, "Segoe Script", "white"), bg="black")
    title.grid(row=0, column=0, padx=380, pady=40)

    boton_jugar = tk.Button(window1, crear_texto("Jugar", 20, "Segoe Script", "white"), width=8, height=1, bg="gray", command=abrir_juego)
    boton_jugar.grid(row=1, column=0, padx=380, pady=0)

    boton_editor = tk.Button(window1, crear_texto("Editor", 20, "Segoe Script", "white"), width=8, height=1, bg="gray", command=abrir_editor)
    boton_editor.grid(row=2, column=0, padx=380, pady=40)

    boton_settings = tk.Button(window1, crear_texto("Settings", 20, "Segoe Script", "white"), width=8, height=1, bg="gray", command=abrir_settings)
    boton_settings.grid(row=3, column=0, padx=380, pady=0)

    boton_puntajes = tk.Button(window1, crear_texto("Puntajes", 20, "Segoe Script", "white"), width=8, height=1, bg="gray", command=abrir_puntajes)
    boton_puntajes.grid(row=4, column=0, padx=380, pady=40)

    boton_exit = tk.Button(window1, crear_texto("Exit", 20, "Segoe Script", "white"), width=8, height=1, bg="gray", command=window1.destroy)
    boton_exit.grid(row=5, column=0, padx=380, pady=0)

    window1.mainloop()


if __name__ == "__main__":
    main()