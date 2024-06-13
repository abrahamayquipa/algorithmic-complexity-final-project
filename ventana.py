# Bibliografia:
# https://stackoverflow.com/questions/25636804/centering-window-python-tkinter

def centrarVentana(root):
    root.update_idletasks()

    # Obtiene dimensiones de la pantalla
    anchoPantalla = root.winfo_screenwidth()
    altoPantalla = root.winfo_screenheight()

    # Obtiene dimensiones de la pantalla
    anchoVentana = root.winfo_width()
    altoVentana = root.winfo_height()

    # Calcula las coordenadas (x, y) para centrar la ventana
    x = (anchoPantalla / 2) - (anchoVentana / 2)
    y = (altoPantalla / 2) - (altoVentana / 2)

    root.geometry('+%d+%d' % (int(x), int(y)))