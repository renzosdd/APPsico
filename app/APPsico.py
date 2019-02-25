from tkinter import *
from tkinter import ttk


""" class interfazPestana:
    def __init__(self,pestanaPrincipal):
        self.gestorPestana=pestanaPrincipal

    def crearInterfaz(self):
        self.pestana=ttk.Frame(self.gestorPestana)
        self.pestana.pack(expand=True, fill=BOTH)
        self.entrySearch=Entry(self.pestana)
        self.entrySearch.grid(row=0, column=0, pady=5,padx=1)
        self.btnSearch=ttk.Button(self.pestana,text="Buscar")
        self.btnSearch.grid(row=0,column=2, pady=5,padx=1) 
        self.listbox1=Listbox(self.pestana)
        self.listbox1.grid(row=1,column=0,columnspan=2)
        self.scllVlist=ttk.Scrollbar(self.pestana,command=self.listbox1.yview)
        self.scllVlist.grid(row=1,column=3, sticky="nsew")
        self.listbox1.config(yscrollcommand=self.scllVlist.set)
        return self.pestana
 """
class Aplicacion:
    # Declaramos una variable para controlar cantidad de de ventanas
    ventana = 0

    def __init__(self):
        #Definicion de ventana del programa
        self.ventanaPrincipal=Tk()
        self.ventanaPrincipal.geometry('500x500+200+50')
        self.ventanaPrincipal.title("APPSico - El bosque")
        self.ventanaPrincipal.resizable(0,0)
        #Definicion Gestor de pestañas
        self.pestanasPrincipal = ttk.Notebook(self.ventanaPrincipal)
        self.pestanasPrincipal.pack(expand=True, fill=BOTH)    
        #Definicion pestaña pacientes
        self.pestanasPrincipal.add(self.crearInterfaz(), text="Pacientes")
        #Definicion pestaña sesiones
        self.pestanasPrincipal.add(self.crearInterfaz(), text="Sesiones")

        #Prueba para abrir nueva ventana
        boton = ttk.Button(self.ventanaPrincipal, text='Abrir', command=self.abrir)
        boton.pack(side=BOTTOM, padx=20, pady=20)


    
        self.ventanaPrincipal.mainloop()
    
    def abrir(self):
        ''' Construye una ventana de diálogo '''
        if (Aplicacion.ventana == 0):
            # Define una nueva ventana de diálogo
            
            self.dialogo = Toplevel()
            
            # Incrementa en 1 el contador de ventanas
            
            Aplicacion.ventana+=1
            

            self.dialogo.geometry('500x500+200+50')
            self.dialogo.resizable(0,0)
            
            # Obtiene identicador de la nueva ventana 
            
            ident = self.dialogo.winfo_id()
            
            # Construye mensaje de la barra de título
            
            titulo = str(Aplicacion.ventana)+": "+str(ident)
            self.dialogo.title(titulo)
            
            # Define el botón 'Cerrar' que cuando sea
            # presionado cerrará (destruirá) la ventana 
            # 'self.dialogo' llamando al método
            # 'self.dialogo.destroy'

            boton = ttk.Button(self.dialogo, text='Cerrar', 
                            command=self.dialogo.destroy)   
            boton.pack(side=BOTTOM, padx=20, pady=20)
            
            # Cuando la ejecución del programa llega a este 
            # punto se utiliza el método wait_window() para
            # esperar que la ventana 'self.dialogo' sea 
            # destruida. 
            # Mientras tanto se atiende a los eventos locales
            # que se produzcan, por lo que otras partes de la
            # aplicación seguirán funcionando con normalidad. 
            # Si hay código después de esta línea se ejecutará
            # cuando la ventana 'self.dialogo' sea cerrada.

            self.ventanaPrincipal.wait_window(self.dialogo)
            Aplicacion.ventana=0

    def crearInterfaz(self):
        self.pestana=ttk.Frame(self.pestanasPrincipal)
        self.pestana.pack(expand=True, fill=BOTH)
        self.entrySearch=Entry(self.pestana)
        self.entrySearch.grid(row=0, column=0, pady=5,padx=1)
        self.btnSearch=ttk.Button(self.pestana,text="Buscar")
        self.btnSearch.grid(row=0,column=2, pady=5,padx=1) 
        self.listbox1=Listbox(self.pestana)
        self.listbox1.grid(row=1,column=0,columnspan=2)
        self.scllVlist=ttk.Scrollbar(self.pestana,command=self.listbox1.yview)
        self.scllVlist.grid(row=1,column=3, sticky="nsew")
        self.listbox1.config(yscrollcommand=self.scllVlist.set)
        return self.pestana

APPSico=Aplicacion()