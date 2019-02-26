from tkinter import *
from tkinter import ttk
import sqlite3 as lite
import sys
from tkinter import messagebox

#Metodo para crear la conexion a la base de datos
def query(sql):
    con = lite.connect('app/APPSico.db')
    with con:
        cur = con.cursor()    
        cur.execute(sql)
        return cur

#Clase pacientes

class Paciente:
    def __init__(self):
        pass

    #Metodo para definir nuevos pacientes
    def alta(self,nombre,apellido,email,tel,notas):
        self.nombre=nombre
        self.apellido=apellido
        self.email=email
        self.tel=tel
        self.notas=notas
        try:
            query('INSERT INTO pacientes (nombre,apellido,mail,telefono,notas) VALUES ("'+self.nombre+'","'+self.apellido+'","'+self.email+'","'+self.tel+'","'+self.notas+'");')
        except:
            pass

    def baja(self,id_paciente):
        self.id=id_paciente
        try:
            query('DELETE FROM pacientes WHERE id_paciente = '+self.id+';')
        except:
            pass

    #Metodo para consultar pacientes pasandole la sentencia SQL
    def consulta(self,sql):
        row=query(sql).fetchall()
        return row


class interfazPacientes:
    def __init__(self,pestanaPrincipal):
        self.gestorPestana=pestanaPrincipal

    def crearInterfazPaciente(self):
        self.pestanaPaciente=ttk.Frame(self.gestorPestana)
        self.pestanaPaciente.pack(expand=True, fill=BOTH)
        self.entryBuscarPaciente=Entry(self.pestanaPaciente)
        self.entryBuscarPaciente.grid(row=0, column=0, pady=5,padx=1)
        self.btnBuscarPaciente=ttk.Button(self.pestanaPaciente,text="Buscar")
        self.btnBuscarPaciente.grid(row=0,column=3, pady=5,padx=1) 
        self.btnRefrescarPacientes=ttk.Button(self.pestanaPaciente,text="Refrescar lista",command=self.refresco)
        self.btnRefrescarPacientes.grid(row=1,column=3, pady=5,padx=1) 
        self.listboxPaciente=Listbox(self.pestanaPaciente)
        self.listboxPaciente.grid(row=1,column=0,columnspan=2)
        self.scllVPaciente=ttk.Scrollbar(self.pestanaPaciente,command=self.listboxPaciente.yview)
        self.scllVPaciente.grid(row=1,column=2, sticky="nsew")
        self.listboxPaciente.config(yscrollcommand=self.scllVPaciente.set)
        self.btnNuevoPaciente = ttk.Button(self.pestanaPaciente, text='Nuevo Paciente', command=self.nuevoPaciente)
        self.btnNuevoPaciente.grid(row=2,column=3)
        self.refresco()
        #Prueba para abrir nueva ventana

        return self.pestanaPaciente
    
    def refresco(self):
        self.pacientes = Paciente()
        self.listapacientes = self.pacientes.consulta("SELECT * FROM pacientes")
        #limpiamoslistview
        self.listboxPaciente.delete(0, END)
        #Refrescamos la lista de pacientes
        count = 0
        for paciente in self.listapacientes:
            self.listboxPaciente.insert(count,paciente[1])
            count+=1

    def nuevoPaciente(self):
        if (Aplicacion.ventana == 0):

            #Creamos una ventana de dialogo
            self.dialogo = Toplevel()
            
            # Incrementa en 1 el contador de ventanas para controlar que solo se abra 1
            Aplicacion.ventana+=1
            
            #self.dialogo.geometry('500x500+200+50')
            self.dialogo.resizable(0,0)
            
            # Obtiene identicador de la nueva ventana       
            #ident = self.dialogo.winfo_id()
            #titulo = str(Aplicacion.ventana)+": "+str(ident)
            self.dialogo.title("Nuevo Paciente")

            nombreLabel=Label(self.dialogo, text="Nombre: ")
            nombreLabel.grid(row=0, column=0, sticky="e", pady=5, padx=1)

            nombretxt=Entry(self.dialogo)
            nombretxt.grid(row=0, column=1, pady=5)

            apellidoLabel=Label(self.dialogo, text="Apellido: ")
            apellidoLabel.grid(row=1, column=0, sticky="e", pady=5, padx=1)

            apellidotxt=Entry(self.dialogo)
            apellidotxt.grid(row=1, column=1, pady=5)

            mailLabel=Label(self.dialogo, text="Correo: ")
            mailLabel.grid(row=2, column=0, sticky="e", pady=5, padx=1)

            mailtxt=Entry(self.dialogo)
            mailtxt.grid(row=2, column=1, pady=5)

            telLabel=Label(self.dialogo, text="Telefono: ")
            telLabel.grid(row=3, column=0, sticky="e", pady=5, padx=1)

            teltxt=Entry(self.dialogo)
            teltxt.grid(row=3, column=1, pady=5)

            comentariosLabel=Label(self.dialogo, text="Notas: ")
            comentariosLabel.grid(row=4, column=0, sticky="e", pady=5, padx=1)

            comentariosText=Text(self.dialogo,height=5,width=16)
            comentariosText.grid(row=4, column=1, sticky="e", pady=5, padx=1)
            scrollVert=Scrollbar(self.dialogo,command=comentariosText.yview)
            scrollVert.grid(row=4,column=2, sticky="nsew")
            comentariosText.config(yscrollcommand=scrollVert.set)

            def altaPaciente():
                nombre = nombretxt.get()
                apellido = apellidotxt.get()
                mail=mailtxt.get()
                telefono=teltxt.get()
                notas=comentariosText.get("1.0",'end-1c')
                try:
                    self.pacientes.alta(nombre,apellido,mail,telefono,notas)
                    messagebox.showinfo("Se inserto correctamente", "El paciente" +nombre+" "+apellido+" fue creado correctamente")
                    nombretxt.set("")
                    apellidotxt.set("")
                    mailtxt.set("")
                    teltxt.set("")
                except:
                    print("Error no se pudo crear")

            botonEnvio=ttk.Button(self.dialogo,text="enviar",command=altaPaciente)              
            botonEnvio.grid(row=5,column=0,columnspan=2)
            boton = ttk.Button(self.dialogo, text='Cerrar',command=self.dialogo.destroy)  
            boton.grid(row=6,column=0,columnspan=2) 
            #self.ventanaPrincipal.wait_window(self.dialogo)
            Aplicacion.ventana=0

class Aplicacion:
    # Declaramos una variable para controlar cantidad de de ventanas
    ventana = 0

    def __init__(self):
        self.pacientes = Paciente()
        #self.listapacientes = self.pacientes.consulta("SELECT * FROM pacientes")
        #Definicion de ventana del programa
        self.ventanaPrincipal=Tk()
        #self.ventanaPrincipal.geometry('500x500+200+50')
        self.ventanaPrincipal.title("APPSico - El bosque")
        self.ventanaPrincipal.resizable(0,0)
        #Definicion Gestor de pestañas
        self.pestanasPrincipal = ttk.Notebook(self.ventanaPrincipal)
        self.pestanasPrincipal.pack(expand=True, fill=BOTH)  
        #Definicion pestaña pacientes
        self.pestanaPaciente=interfazPacientes(self.pestanasPrincipal)
        self.pestanasPrincipal.add(self.pestanaPaciente.crearInterfazPaciente(), text="Pacientes")
        #Definicion pestaña sesiones
        self.pestanaSesiones=interfazPacientes(self.pestanasPrincipal)
        self.pestanasPrincipal.add(self.pestanaSesiones.crearInterfazPaciente(), text="Sesiones")
    
        self.ventanaPrincipal.mainloop()

APPSico=Aplicacion()