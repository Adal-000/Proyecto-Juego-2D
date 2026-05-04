import tkinter as tk

def main():
    window1 = tk.Tk()

    p_ancho = (window1.winfo_screenwidth())
    p_alto = (window1.winfo_screenheight())
    x = (p_ancho - p_ancho // 2) - 1150 // 2
    y = (p_alto - p_alto // 2) - 800 // 2


    window1.geometry(f"{1150}x{700}+{x}+{y}")
    window1.title("Main Menu")
    window1.resizable(False, False)

    def GoexitR():
        Exit()

    def GomapsR():
        maps() 

    def GoeditorR():
        editor()

    def GocsettingsR():
        settings()
        

    exit = tk.Button(window1, text="Exit", width=20, height=5, bg="red", command=GoexitR)
    exit.grid(row=0, column=0, padx=200, pady=80)

    maps= tk.Button(window1, text="", width=20, height=5, bg="red", command=GomapsR)
    maps.grid(row=1, column=0, padx=200, pady=80)

    editor = tk.Button(window1, text="Editor", width=20, height=5, bg="red", command=GoeditorR)
    editor.grid(row=2, column=0, padx=200, pady=80)

    settings = tk.Button(window1, text="Settings", width=20, height=5, bg="red", command=GocsettingsR)
    settings.grid(row=3, column=0, padx=200, pady=80)

    window1.mainloop()

main()