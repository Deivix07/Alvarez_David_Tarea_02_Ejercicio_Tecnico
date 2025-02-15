# main.py
from database import crear_tablas
from ui_seleccion_tipo import mostrar_seleccion_tipo

if __name__ == "__main__":
    # Crear las tablas en la base de datos (si no existen)
    crear_tablas()
    
    # Mostrar la pantalla de selección de tipo de usuario
    mostrar_seleccion_tipo()