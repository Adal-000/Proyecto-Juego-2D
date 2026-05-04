import tkinter as tk

def main():

    #==============================================#
    #interfaz principal
    #==============================================#

    window1 = tk.Tk()

    p_ancho = (window1.winfo_screenwidth())
    p_alto = (window1.winfo_screenheight())
    x = (p_ancho - p_ancho // 2) - 1150 // 2
    y = (p_alto - p_alto // 2) - 800 // 2


    window1.geometry(f"{1150}x{700}+{x}+{y}")
    window1.title("Main Menu")
    window1.resizable(False, False)
    window1.configure(bg="black")

    #==============================================#
    #funciones a usar
    #==============================================#

    def crear_texto(ventana, texto, tamano=20, tipo_fuente="Arial Rounded MT Bold", color="black"): # crea texto con sus respectivas entradas

        fuente_default = "Arial"        # si no se indica fuente

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
            "Cambria"
        ]                                       # fuentes a usar en la funcion

        if tipo_fuente in fuentes_disponibles:
            fuente_final = tipo_fuente
        else:
            fuente_final = fuente_default

        return {
            "text": texto,
            "font": (fuente_final, tamano, "bold"),
            "fg": color
        }

    def exit():
        window1.destroy()

    def Gojugar():
        jugar() 

    def Goeditor():
        editor()

    def Gocsettings():
        settings()

    #==============================================#
    #botones y mas
    #==============================================#

    title = tk.Label(window1, crear_texto(window1, "Juego de Plataformas", 30, "Segoe Script", "white"), bg="black")
    title.grid(row=0, column=0, padx=380, pady=40)

    jugar= tk.Button(window1, crear_texto(window1, "Jugar", 20, "Segoe Script", "white"), width=8, height=1, bg="gray", command=Gojugar)
    jugar.grid(row=1, column=0, padx=380, pady=0)

    editor = tk.Button(window1, crear_texto(window1, "Editor", 20, "Segoe Script", "white"), width=8, height=1, bg="gray", command=Goeditor)
    editor.grid(row=2, column=0, padx=380, pady=40)

    settings = tk.Button(window1, crear_texto(window1, "Settings", 20, "Segoe Script", "white"), width=8, height=1, bg="gray", command=Gocsettings)
    settings.grid(row=3, column=0, padx=380, pady=0)

    exit = tk.Button(window1, crear_texto(window1, "Exit", 20, "Segoe Script", "white"), width=8, height=1, bg="gray", command=exit)
    exit.grid(row=4, column=0, padx=380, pady=40)

    window1.mainloop()

main()