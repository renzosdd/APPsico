from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
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
    def __init__(self,ventanaPrincipal):
        self.ventanaPrincipal=ventanaPrincipal

    def InterfazPrincipal(self):
        self.frmInterfazPrincipal=ttk.LabelFrame(self.ventanaPrincipal,text="Pacientes")
        self.frmInterfazPrincipal.pack(expand=True, fill=BOTH)
        #Campo de busqueda
        self.entryBuscarPaciente=Entry(self.frmInterfazPrincipal)
        self.entryBuscarPaciente.grid(row=0, column=0, pady=5,padx=1,sticky="W")
        self.entryBuscarPaciente.config(width=45)
        #Boton Buscar
        self.btnBuscarPaciente=ttk.Button(self.frmInterfazPrincipal,text="Buscar",command=lambda:self.buscarPaciente(1))
        self.btnBuscarPaciente.grid(row=0,column=2, pady=5,padx=1,sticky="E") 
        #Boton Refrescar
        self.btnRefrescarPacientes=ttk.Button(self.frmInterfazPrincipal,text="Refrescar",command=lambda:self.buscarPaciente(2))
        self.btnRefrescarPacientes.grid(row=0,column=1, pady=5,padx=1,sticky="E") 
        #Lista de Pacientes
        self.treePaciente=ttk.Treeview(self.frmInterfazPrincipal)
        self.treePaciente.grid(row=1,column=0,columnspan=4) 
        self.treePaciente["columns"]=("one","two","three")
        self.treePaciente.column("#0", width=40, minwidth=10, stretch=NO)
        self.treePaciente.column("one", width=150, minwidth=150, stretch=NO)
        self.treePaciente.column("two", width=150, minwidth=150)
        self.treePaciente.column("three", width=200, minwidth=150, stretch=NO)
        self.treePaciente.heading("#0",text="ID",anchor=W)
        self.treePaciente.heading("one", text="Nombre",anchor=W)
        self.treePaciente.heading("two", text="Apellido",anchor=W)
        self.treePaciente.heading("three", text="email",anchor=W)
        self.scllVPaciente=ttk.Scrollbar(self.frmInterfazPrincipal,command=self.treePaciente.yview)
        self.scllVPaciente.grid(row=1,column=4, sticky="nsew")
        self.treePaciente.config(yscrollcommand=self.scllVPaciente.set)
        #Boton nuevo Paciente
        self.btnNuevoPaciente = ttk.Button(self.frmInterfazPrincipal, text='Nuevo Paciente', command=self.nuevoPaciente)
        self.btnNuevoPaciente.grid(row=2,column=3)
        #Boton eliminar Paciente
        self.btnEliminarPaciente = ttk.Button(self.frmInterfazPrincipal, text='Eliminar Paciente', command=self.eliminarPaciente)
        self.btnEliminarPaciente.grid(row=2,column=2)
        #Boton visualizar ficha Paciente
        self.btnFichaPaciente = ttk.Button(self.frmInterfazPrincipal, text='Ficha Paciente', command=self.fichaPaciente)
        self.btnFichaPaciente.grid(row=2,column=1)
        #Refrescamos lista de pacientes
        self.buscarPaciente(2)
        #Retornamos el frame con todos los widgets cargados
        return self.frmInterfazPrincipal
    
    def buscarPaciente(self,modo):
        self.pacientes = Paciente()
        #Modo busqueda
        if (modo == 1):
            busqueda=self.entryBuscarPaciente.get()
            self.listapacientes = self.pacientes.consulta("SELECT * FROM pacientes WHERE nombre LIKE '%"+busqueda+"%' OR apellido LIKE '%"+busqueda+"%' OR mail LIKE '%"+busqueda+"%'")
        #Modo para encontrar a todos los pacientes
        elif(modo == 2):
            self.listapacientes = self.pacientes.consulta("SELECT * FROM pacientes")
        for entrada in self.treePaciente.get_children():
            self.treePaciente.delete(entrada)
        for paciente in self.listapacientes:
            self.treePaciente.insert('', 'end', text=paciente[0], values=(paciente[1],paciente[2],paciente[3]),iid=paciente[0])

    def eliminarPaciente(self):
        pacientes = Paciente()
        idPacienteSel = self.treePaciente.focus() 
        try:
            pacientes.baja(idPacienteSel)
            self.buscarPaciente(2)
            messagebox.showinfo("Se elimino correctamente", "El paciente fue eliminado correctamente")
        except:
            print("Error")

    def fichaPaciente(self):
        idPacienteSel = self.treePaciente.focus()
        if (Aplicacion.ventana == 0 and idPacienteSel != ""):
            pacienteSel= Paciente().consulta("SELECT * FROM pacientes WHERE id_paciente="+idPacienteSel)
            self.dialogoFichaPaciente = Toplevel()
            # Incrementa en 1 el contador de ventanas para controlar que solo se abra 1
            Aplicacion.ventana+=1
            self.dialogoFichaPaciente.resizable(0,0)
            self.dialogoFichaPaciente.title("Ficha del paciente - "+pacienteSel[0][1]+" "+pacienteSel[0][2])
            self.FrmFichaPaciente=ttk.LabelFrame(self.dialogoFichaPaciente,text="Ficha del paciente - "+pacienteSel[0][1]+" "+pacienteSel[0][2])
            self.FrmFichaPaciente.pack(expand=True, fill=BOTH)
             #Lista de Pacientes
            self.treeFichaPaciente=ttk.Treeview(self.FrmFichaPaciente)
            self.treeFichaPaciente.grid(row=1,column=0,columnspan=4) 
            self.treeFichaPaciente["columns"]=("one","two")
            self.treeFichaPaciente.column("#0", width=150, minwidth=10, stretch=NO)
            self.treeFichaPaciente.column("one", width=150, minwidth=150, stretch=NO)
            self.treeFichaPaciente.column("two", width=350, minwidth=150)
            #self.treeFichaPaciente.column("three", width=200, minwidth=150, stretch=NO)
            self.treeFichaPaciente.heading("#0",text="Fecha y hora inicio",anchor=W)
            self.treeFichaPaciente.heading("one", text="Fecha y hora Fin",anchor=W)
            self.treeFichaPaciente.heading("two", text="Notas",anchor=W)
            #self.treeFichaPaciente.heading("three", text="Hora fin",anchor=W)
            self.scllVPaciente=ttk.Scrollbar(self.FrmFichaPaciente,command=self.treeFichaPaciente.yview)
            self.scllVPaciente.grid(row=1,column=4, sticky="nsew")
            self.treeFichaPaciente.config(yscrollcommand=self.scllVPaciente.set)
            boton = ttk.Button(self.FrmFichaPaciente, text='Cerrar', command=self.dialogoFichaPaciente.destroy)
            boton.grid(row=5, column=1)
            self.listaSesiones = query("SELECT pacientes.nombre,pacientes.apellido,sesiones.inicio,sesiones.fin,sesiones.notas FROM pacientes INNER JOIN sesiones ON pacientes.id_paciente=sesiones.id_paciente WHERE pacientes.id_paciente="+idPacienteSel).fetchall()
            for entrada in self.treeFichaPaciente.get_children():
                self.treeFichaPaciente.delete(entrada)
            for sesion in self.listaSesiones:
                self.treeFichaPaciente.insert('', 'end', text=sesion[2], values=(sesion[3],sesion[4]))



            Aplicacion.ventana = 0

    def nuevoPaciente(self):
        if (Aplicacion.ventana == 0):
            #Creamos una ventana de dialogoNuevoPaciente
            self.dialogoNuevoPaciente = Toplevel()
            # Incrementa en 1 el contador de ventanas para controlar que solo se abra 1
            Aplicacion.ventana+=1
            #self.dialogoNuevoPaciente.geometry('500x500+200+50')
            self.dialogoNuevoPaciente.resizable(0,0)
            # Obtiene identicador de la nueva ventana       
            #ident = self.dialogoNuevoPaciente.winfo_id()
            #titulo = str(Aplicacion.ventana)+": "+str(ident)
            self.dialogoNuevoPaciente.title("Nuevo Paciente")
            self.FrmNvoPaciente=ttk.LabelFrame(self.dialogoNuevoPaciente,text="Alta paciente")
            self.FrmNvoPaciente.pack(expand=True, fill=BOTH)


            nombreLabel=Label(self.FrmNvoPaciente, text="Nombre: ")
            nombreLabel.grid(row=0, column=0, sticky="e", pady=5, padx=1)

            nombretxt=Entry(self.FrmNvoPaciente)
            nombretxt.grid(row=0, column=1, pady=5)

            apellidoLabel=Label(self.FrmNvoPaciente, text="Apellido: ")
            apellidoLabel.grid(row=1, column=0, sticky="e", pady=5, padx=1)

            apellidotxt=Entry(self.FrmNvoPaciente)
            apellidotxt.grid(row=1, column=1, pady=5)

            mailLabel=Label(self.FrmNvoPaciente, text="Correo: ")
            mailLabel.grid(row=2, column=0, sticky="e", pady=5, padx=1)

            mailtxt=Entry(self.FrmNvoPaciente)
            mailtxt.grid(row=2, column=1, pady=5)

            telLabel=Label(self.FrmNvoPaciente, text="Telefono: ")
            telLabel.grid(row=3, column=0, sticky="e", pady=5, padx=1)

            teltxt=Entry(self.FrmNvoPaciente)
            teltxt.grid(row=3, column=1, pady=5)

            comentariosLabel=Label(self.FrmNvoPaciente, text="Notas: ")
            comentariosLabel.grid(row=4, column=0, sticky="e", pady=5, padx=1)

            comentariosText=Text(self.FrmNvoPaciente,height=5,width=16)
            comentariosText.grid(row=4, column=1, sticky="e", pady=5, padx=1)
            scrollVert=Scrollbar(self.FrmNvoPaciente,command=comentariosText.yview)
            scrollVert.grid(row=4,column=2, sticky="nsew")
            comentariosText.config(yscrollcommand=scrollVert.set)

            def altaPaciente():
                nombre = nombretxt.get()
                apellido = apellidotxt.get()
                mail = mailtxt.get()
                telefono = teltxt.get()
                notas = comentariosText.get("1.0",'end-1c')
                try:
                    self.pacientes.alta(nombre, apellido, mail, telefono, notas)
                    messagebox.showinfo("Se creo correctamente", "El paciente " +nombre+" "+apellido+" fue creado correctamente")
                except:
                    messagebox.showinfo("Error al crear el paciente", "No se pudo crear")
                self.buscarPaciente(2)
            botonEnvio = ttk.Button(self.FrmNvoPaciente, text="crear", command=altaPaciente)            
            botonEnvio.grid(row=5, column=0)
            #self.ventanaPrincipal.wait_window(self.dialogoNuevoPaciente)
            Aplicacion.ventana = 0

class Aplicacion:
    #Variable para controlar cantidad de de ventanas
    ventana = 0

    def __init__(self):
        #Definicion de ventana del programa
        self.ventanaPrincipal=Tk()
        self.ventanaPrincipal.title("APPSico - El bosque")
        self.ventanaPrincipal.resizable(0,0)
        interfazPacientes(self.ventanaPrincipal).InterfazPrincipal()
        self.ventanaPrincipal.mainloop()


APPSico=Aplicacion()