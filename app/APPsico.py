from tkinter import *
import Base as B
import FrontEnd as F


class Aplicacion:
    def __init__(self):
        #Definicion de ventana del programa
        self.ventanaPrincipal = Tk()
        self.ventanaPrincipal.title("APPSico - El Bosque")
        self.ventanaPrincipal.resizable(0, 0)
        F.IfazPrincipal(self.ventanaPrincipal).get()
        self.ventanaPrincipal.mainloop()

APPSico = Aplicacion()