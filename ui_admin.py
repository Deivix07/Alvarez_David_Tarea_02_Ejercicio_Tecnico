# ui_admin.py
from tkinter import Tk, Label

def open_admin_dashboard():
    admin_window = Tk()
    admin_window.title("Panel del Administrador")
    
    Label(admin_window, text="Bienvenido Administrador").pack()
    # Aquí puedes agregar más widgets para gestionar todas las citas