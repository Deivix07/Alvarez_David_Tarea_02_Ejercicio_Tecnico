import os, sys

# Obtiene la ruta de la carpeta de recursos dependiendo de si estamos en un archivo empaquetado o no
def obtener_ruta_recurso(ruta_recurso):
    if getattr(sys, 'frozen', False):  # Si estamos ejecutando el .exe
        return os.path.join(sys._MEIPASS, ruta_recurso)
    else:  # Si estamos ejecutando el código fuente
        return os.path.join(os.path.dirname(__file__), ruta_recurso)