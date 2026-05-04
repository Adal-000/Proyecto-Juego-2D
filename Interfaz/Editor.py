from Main import *


def editor():
    window3 = tk.Toplevel(main)
    p_ancho = (window3.winfo_screenwidth())
    p_alto = (window3.winfo_screenheight())
    x = (p_ancho - p_ancho // 2) - 1150 // 2
    y = (p_alto - p_alto // 2) - 800 // 2

    window3.geometry(f"{1150}x{700}+{x}+{y}")
    window3.title("Editor")
    window3.resizable(False, False)