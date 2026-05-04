from Main import * 


def jugar():
    window2 = tk.Toplevel(main)
    p_ancho = (window2.winfo_screenwidth())
    p_alto = (window2.winfo_screenheight())
    x = (p_ancho - p_ancho // 2) - 1150 // 2
    y = (p_alto - p_alto // 2) - 800 // 2

    window2.geometry(f"{1150}x{700}+{x}+{y}")
    window2.title("Maps")
    window2.resizable(False, False)