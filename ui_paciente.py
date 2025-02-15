# ui_paciente.py
from tkinter import Tk, Label

def open_patient_dashboard():
    patient_window = Tk()
    patient_window.title("Panel del Paciente")
    
    Label(patient_window, text="Bienvenido Paciente").pack()
    # Aquí puedes agregar más widgets para gestionar citas