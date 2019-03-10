#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk, messagebox
import BackEnd as B
import FrontEnd as F

# Gestor de geometría (pack)

class Aplicacion():
    def __init__(self):
        self.raiz = Tk()
        self.raiz.title("APPSico - El Bosque")
        logo = PhotoImage(file="APPsico.png")
        Label(self.raiz, compound = CENTER, text="", image=logo).pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.raiz.iconbitmap('APPsico.ico')
        self.lblUsuario = ttk.Label(self.raiz, text="Usuario:")
        self.lblClave = ttk.Label(self.raiz, text="Contraseña:")
        self.usuario = StringVar()
        self.clave = StringVar()
        
        self.txtUsuario = ttk.Entry(self.raiz, 
                                textvariable=self.usuario, 
                                width=30)
        self.txtClave = ttk.Entry(self.raiz, 
                                textvariable=self.clave, 
                                width=30, show="*")
        self.separador = ttk.Separator(self.raiz, orient=HORIZONTAL)
        
        self.btnAceptar = ttk.Button(self.raiz, text="Aceptar", 
                                 command=self.aceptar)
        self.btnCancelar = ttk.Button(self.raiz, text="Cancelar", 
                                 command=quit)
                                         
        self.lblUsuario.pack(side=TOP, fill=BOTH, expand=True, 
                        padx=5, pady=5)
        self.txtUsuario.pack(side=TOP, fill=X, expand=True, 
                         padx=5, pady=5)
        self.lblClave.pack(side=TOP, fill=BOTH, expand=True, 
                        padx=5, pady=5)
        self.txtClave.pack(side=TOP, fill=X, expand=True, 
                         padx=5, pady=5)
        self.separador.pack(side=TOP, fill=BOTH, expand=True, 
                         padx=5, pady=5)
        self.btnAceptar.pack(side=LEFT, fill=BOTH, expand=True, 
                         padx=5, pady=5)
        self.btnCancelar.pack(side=RIGHT, fill=BOTH, expand=True, 
                         padx=5, pady=5)
        
        self.txtUsuario.focus_set()
        self.raiz.mainloop()
    
    def aceptar(self):
        try:
            listaUsuarios=B.query("SELECT * FROM usuarios WHERE usuario='"+self.usuario.get().lower()+"'").fetchall()
            if(listaUsuarios[0][1] == self.clave.get()):
                self.raiz.withdraw()
                F.IfazPrincipal(self.raiz,self.usuario.get().lower())
                self.clave.set("")
            else:
                messagebox.showinfo("Error", "Usuario o clave invalida - Intentelo nuevamente")
                self.clave.set("")
                self.txtClave.focus_set()
        except:
            messagebox.showinfo("Error", "Usuario o clave invalida - Intentelo nuevamente")
            self.clave.set("")
            self.txtClave.focus_set()
        
def main():
    Aplicacion()
    return 0

if __name__ == '__main__':
    main()