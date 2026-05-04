from Main import *


def settings():
    window4 = tk.Toplevel(main)
    p_ancho = (window4.winfo_screenwidth())
    p_alto = (window4.winfo_screenheight())
    x = (p_ancho - p_ancho // 2) - 1150 // 2
    y = (p_alto - p_alto // 2) - 800 // 2

    window4.geometry(f"{1150}x{700}+{x}+{y}")
    window4.title("Settings")
    window4.resizable(False, False)