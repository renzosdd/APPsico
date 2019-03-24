from tkinter import *
from tkinter import ttk, messagebox
from tkinter import scrolledtext as st
from tkinter.ttk import *
import sqlite3

con = sqlite3.connect('APPSico.db')

def query(sql):
        with con:
                cur = con.cursor()
                cur.execute(sql)
                return cur

class Admin():
    def __init__(self):
        self.raiz = Tk()
        self.raiz.title("APPSico - Panel de Administrador - El Bosque ")
        self.raiz.resizable(0,0)
        logo = PhotoImage(file="APPsico-Admin.png")
        Label(self.raiz, compound = CENTER, text="", image=logo).pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.raiz.iconbitmap('APPsico.ico')
        self.lblUsuario = ttk.Label(self.raiz, text="Usuario:")
        self.lblClave = ttk.Label(self.raiz, text="Contraseña:")
        self.lblRepetirClave = ttk.Label(self.raiz, text="Repita contraseña:")
        self.usuario = StringVar()
        self.clave = StringVar()
        self.claveRepetida = StringVar()

        self.txtUsuario = ttk.Entry(self.raiz, textvariable=self.usuario, width=30)
        self.txtClave = ttk.Entry(self.raiz, textvariable=self.clave, width=30, show="*")
        self.txtRepetirClave = ttk.Entry(self.raiz, textvariable=self.claveRepetida, width=30, show="*")
        self.separador = ttk.Separator(self.raiz, orient=HORIZONTAL)
        self.btnCrear = ttk.Button(self.raiz, text="Crear Usuario", command=self.crear)
        self.btnhabilitar = ttk.Button(self.raiz, text="Des/Habilitar",command=self.habilitar)
        self.btnModificar = ttk.Button(self.raiz, text="Modificar clave",command=self.modificar)
        self.btnCancelar = ttk.Button(self.raiz, text="Salir",command=self.raiz.quit)
        self.btnListado = ttk.Button(self.raiz, text="Listado",command=self.listado)

        self.lblUsuario.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.txtUsuario.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
        self.lblClave.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.txtClave.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
        self.lblRepetirClave.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.txtRepetirClave.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
        self.separador.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.btnCrear.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        self.btnCancelar.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)
        self.btnhabilitar.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)
        self.btnModificar.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        self.btnListado.pack(side=BOTTOM, fill=BOTH, expand=True, padx=5, pady=5)

        self.txtUsuario.focus_set()
        self.raiz.mainloop()

    def listado(self):
        listaUsuarios=query("SELECT * FROM usuarios").fetchall()
        for usuario in listaUsuarios:
            if (usuario[2]==0):
                print(str(usuario[0])+" - Deshabilitado" )
            else:
                print(str(usuario[0])+" - Habilitado" )
    def crear(self):
            listaUsuarios=query("SELECT * FROM usuarios WHERE usuario='"+self.usuario.get().lower()+"'").fetchall()
            if(listaUsuarios == []):
                if(self.validar(self.clave.get()) and self.validar(self.claveRepetida.get())):
                    if(self.clave.get()==self.claveRepetida.get()):
                        query("INSERT INTO usuarios VALUES ('"+self.usuario.get().lower()+"','"+self.clave.get()+"') ")
                        self.clave.set("")
                        self.claveRepetida.set("")
                        messagebox.showinfo("Éxito", "Usuario "+self.usuario.get()+" creado correctamente")
                    else:
                        messagebox.showerror("Error", "Las claves no coinciden")
            else:
                self.clave.set("")
                self.claveRepetida.set("")
                self.txtClave.focus_set()
                messagebox.showerror("Error", "Usuario ya existente - Intentelo nuevamente")

    def validar(self,password):

        validar=False #que se vayan cumpliendo los requisitos uno a uno.
        largo=len(password) #Calcula la longitud de la contraseña
        espacio=False  #variable para identificar espacios
        mayuscula=False #variable para identificar letras mayúsculas
        minuscula=False #variable para contar identificar letras minúsculas
        numeros=False #variable para identificar números
        correcto=True #verifica que hayan mayuscula, minuscula, numeros y no alfanuméricos
        
        for carac in password: #ciclo for que recorre caracter por caracter en la contraseña

            if carac.isspace()==True: #Saber si el caracter es un espacio
                espacio=True #si encuentra un espacio se cambia el valor user

            if carac.isupper()== True: #saber si hay mayuscula
                mayuscula=True #acumulador o contador de mayusculas
                
            if carac.islower()== True: #saber si hay minúsculas
                minuscula=True #acumulador o contador de minúsculas
                
            if carac.isdigit()== True: #saber si hay números
                numeros=True #acumulador o contador de numeros
                            
        if espacio==True: #hay espacios en blanco
            messagebox.showinfo("Error", "La clave no puede contener espacios en blanco")
        else:
            validar=True #se cumple el primer requisito que no hayan espacios
                       
        if largo <8 and validar==True:
            messagebox.showinfo("Error", "La clave tiene que ser minimo de 8 digitos")
            validar=False #cambia a Flase si no se cumple el requisito móinimo de caracteres

        if mayuscula == True and minuscula ==True and numeros == True and validar ==True:
            validar = True #Cumple el requisito de tener mayuscula, minuscula y numeros
        else:
            correcto=False #uno o mas requisitos de mayuscula, minuscula, numeros y no alfanuméricos no se cumple
           
        if validar == True and correcto==False:
            messagebox.showerror("Error","La contraseña elegida no es segura: debe contener minimo 8 digitos, letras minúsculas, mayúsculas y números")

        if validar == True and correcto ==True:
           return True


    def habilitar(self):
        listaUsuarios=query("SELECT * FROM usuarios WHERE usuario='"+self.usuario.get().lower()+"'").fetchall()
        if(listaUsuarios == []):
            messagebox.showerror("Error", "No existe el usuario "+self.usuario.get().lower()+" - Intentelo nuevamente")
        else:
            if(listaUsuarios[0][2]==1):
                resultado = messagebox.askquestion("Eliminar", "¿Esta seguro que desea deshabilitar al usuario "+self.usuario.get().lower()+"?", icon='warning')
                if resultado == 'yes':
                    query("UPDATE usuarios SET habilitado = 0 WHERE usuario='"+self.usuario.get().lower()+"';")
                    messagebox.showinfo("Éxito","Se deshabilitó el Usuario "+self.usuario.get().lower())
            else:
                resultado = messagebox.askquestion("Eliminar", "¿Esta seguro que desea habilitar al usuario "+self.usuario.get().lower()+"?", icon='warning')
                if resultado == 'yes':
                    query("UPDATE usuarios SET habilitado = 1 WHERE usuario='"+self.usuario.get().lower()+"';")
                    messagebox.showinfo("Éxito","Se habilitó el Usuario "+self.usuario.get().lower())
    
    def modificar(self):
        listaUsuarios=query("SELECT * FROM usuarios WHERE usuario='"+self.usuario.get().lower()+"'").fetchall()
        if(listaUsuarios == []):
            messagebox.showerror("Error", "Usuario no existente - Intentelo nuevamente")
        else:
            resultado = messagebox.askquestion("Modificar", "¿Esta seguro que desea modificar la contraseña del usuario "+self.usuario.get().lower()+"?", icon='warning')
            if resultado == 'yes':
                    if(self.validar(self.clave.get()) and self.validar(self.claveRepetida.get())):
                        if(self.clave.get()==self.claveRepetida.get()):
                            query("UPDATE usuarios SET clave = '"+self.clave.get()+"' WHERE usuario='"+self.usuario.get().lower()+"';")
                            messagebox.showinfo("Éxito","Se modifico la clave del Usuario "+self.usuario.get().lower())
                        else:
                            messagebox.showerror("Error", "Las claves no coinciden")

Admin()