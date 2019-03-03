from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import sys
import BackPacientes as P
import BackSesiones as S
from tkinter import messagebox

class IfazPrincipal:
    def __init__(self, ventanaPrincipal):
        self.ventanaPrincipal = ventanaPrincipal
        self.pacientes = P.Paciente()
        self.sesiones=S.Sesion()
        self.ventanas = 0
        self.frmIfazPrincipal = ttk.LabelFrame(self.ventanaPrincipal, text="Pacientes")
        self.frmIfazPrincipal.pack(expand=True, fill=BOTH)
        #Campo de busqueda
        self.txtBuscarPaciente = Entry(self.frmIfazPrincipal)
        self.txtBuscarPaciente.grid(row=0, column=0, pady=5, padx=1, sticky="ew")
        self.txtBuscarPaciente.config(width=45)
        #Boton Buscar
        self.btnBuscarPaciente = ttk.Button(self.frmIfazPrincipal, text="Buscar", command=lambda: self.buscarPaciente(1))
        self.btnBuscarPaciente.grid(row=0, column=1, pady=5, padx=1, sticky="nsew")
        #Boton Refrescar
        self.btnRefrescarPacientes = ttk.Button(self.frmIfazPrincipal, text="Reestablecer", command=lambda: self.buscarPaciente(2))
        self.btnRefrescarPacientes.grid(row=0, column=2, pady=5, padx=1, sticky="nsew")
        #Lista de Pacientes
        self.treePaciente = ttk.Treeview(self.frmIfazPrincipal, selectmode='browse')
        self.treePaciente.grid(row=1, column=0, columnspan=4)
        self.treePaciente["columns"] = ("1", "2", "3")
        self.treePaciente.column("#0", width=120, minwidth=120, stretch=NO)
        self.treePaciente.column("1", width=150, minwidth=150, stretch=NO)
        self.treePaciente.column("2", width=200, minwidth=150)
        self.treePaciente.column("3", width=150, minwidth=150, stretch=NO)
        self.treePaciente.heading("#0", text="Nombre", anchor=W)
        self.treePaciente.heading("1", text="Apellido", anchor=W)
        self.treePaciente.heading("2", text="Email", anchor=W)
        self.treePaciente.heading("3", text="Teléfono", anchor=W)
        self.scllPaciente = ttk.Scrollbar(self.frmIfazPrincipal, command=self.treePaciente.yview)
        self.scllPaciente.grid(row=1, column=4, sticky="nsew")
        self.treePaciente.config(yscrollcommand=self.scllPaciente.set)
        #Boton nuevo Paciente
        self.btnifazFichaPaciente = ttk.Button(self.frmIfazPrincipal, text='Nuevo Paciente', command=self.ifazFichaPaciente)
        self.btnifazFichaPaciente.grid(row=2, column=3, sticky="ew")
        #Boton visualizar Paciente
        self.btnvisualizarPacientes = ttk.Button(self.frmIfazPrincipal, text='Visualizar Paciente', command=self.visualizarPacientes)
        self.btnvisualizarPacientes.grid(row=2, column=2, sticky="ew")
        #Boton visualizar sesiones
        self.btnifazSesiones = ttk.Button(self.frmIfazPrincipal, text='Sesiones', command=self.ifazSesiones)
        self.btnifazSesiones.grid(row=2, column=0, sticky="ew")
        #Refrescamos lista de pacientes
        self.buscarPaciente(2)
        #Inicializamos el menu contextual
        self.menu()

    def menu(self):
        self.aMenu = Menu(self.frmIfazPrincipal, tearoff=0)
        self.treePaciente.bind('<Button-3>', self.popup)
        self.aMenu.add_command(label='Sesiones', command=self.ifazSesiones)
        self.aMenu.add_command(label='Ficha del paciente', command=self.visualizarPacientes)

    def popup(self, event):
        if self.treePaciente.focus():
            self.aMenu.post(event.x_root, event.y_root)
            self.tree_item = self.treePaciente.focus()

    def get(self):
        return self.frmIfazPrincipal

    def buscarPaciente(self, modo, *kwarg):
        #Modo busqueda
        if modo == 1:
            busqueda = self.txtBuscarPaciente.get()
            listapacientes = self.pacientes.consulta("SELECT * FROM pacientes WHERE nombre LIKE '%"+busqueda+"%' OR apellido LIKE '%"+busqueda+"%' OR mail LIKE '%"+busqueda+"%'")
        #Modo para encontrar a todos los pacientes
        elif modo == 2:
            listapacientes = self.pacientes.consulta("SELECT * FROM pacientes")
        #Busqueda de paciente pasando un ID
        elif modo == 3 and kwarg:
            id_sel = str(kwarg[0])
            paciente_sel = self.pacientes.consulta('SELECT * FROM pacientes WHERE id_paciente = '+id_sel+';')
            return paciente_sel
        for entrada in self.treePaciente.get_children():
            self.treePaciente.delete(entrada)
        for paciente in listapacientes:
            self.treePaciente.insert('', 'end', text=paciente[1], values=(paciente[2], paciente[3], paciente[4]), iid=paciente[0])

    def nuevoPaciente(self, txtComentarios):
        try:
            self.paciente.alta(self.nombre.get(), self.apellido.get(), self.email.get(), self.telefono.get(), txtComentarios)
            messagebox.showinfo("Se creo correctamente", "El paciente " +self.nombre.get()+" "+self.apellido.get()+" fue creado correctamente")
            self.cerrarDialogo(self.dlgNvoPaciente)
        except:
            messagebox.showinfo("Error al crear el paciente", "No se pudo crear")
        self.buscarPaciente(2)

    def visualizarPacientes(self):
        if self.treePaciente.focus():
            self.ifazFichaPaciente(self.treePaciente.focus())
        else:
            messagebox.showinfo("Error", "No se seleccionó ningún paciente")

    def modificarPacientes(self, id_paciente, txtComentarios):
        try:
            self.paciente.modificar(str(id_paciente), self.nombre.get(), self.apellido.get(), self.email.get(), self.telefono.get(), txtComentarios)
            messagebox.showinfo("Se Modifico correctamente", "El paciente " +self.nombre.get()+" "+self.apellido.get()+" se modifico correctamente")
            self.buscarPaciente(2)
            self.cerrarDialogo(self.dlgNvoPaciente)
        except:
            messagebox.showinfo("Error al crear el paciente", "No se pudo crear")

    def eliminarPaciente(self, id_paciente):
        resultado = messagebox.askquestion("Eliminar", "¿Esta seguro que desea eliminar al paciente?", icon='warning')
        if resultado == 'yes':
            try:
                print(str(id_paciente))
                self.paciente.baja(str(id_paciente))
                messagebox.showinfo("Éxito","Se elimino correctamente")
                self.buscarPaciente(2)
                self.cerrarDialogo(self.dlgNvoPaciente)
            except:
                messagebox.showinfo("Error","No se pudo eliminar")
        else:
            pass

    def cerrarDialogo(self,dialogo):
        dialogo.destroy()
        self.ventanas=0
        self.ventanaPrincipal.state(newstate='normal')
        self.ventanaPrincipal.deiconify()

    def ifazFichaPaciente(self, *kargs):
        self.habilitado = 0
        #Ocultamos la ventanaPrincipal mientras esta el dialogo abierto
        self.ventanaPrincipal.withdraw()
        self.nombre = StringVar()
        self.apellido = StringVar()
        self.email = StringVar()
        self.telefono = StringVar()
        #Creamos una ventana
        self.dlgNvoPaciente = Toplevel()
        #Hacemos que el protocolo de cierre de dialogo llame al metodo CerrarDialogo
        self.dlgNvoPaciente.protocol("WM_DELETE_WINDOW", lambda: self.cerrarDialogo(self.dlgNvoPaciente))
        self.dlgNvoPaciente.resizable(0,0)
        self.FrmNvoPaciente = ttk.LabelFrame(self.dlgNvoPaciente, text="Alta paciente")
        self.FrmNvoPaciente.pack(expand=True, fill=BOTH)
        lblNombre = Label(self.FrmNvoPaciente, text="Nombre: ")
        lblNombre.grid(row=0, column=0, sticky="e", pady=5, padx=1)
        txtNombre = Entry(self.FrmNvoPaciente, textvariable=self.nombre)
        txtNombre.grid(row=0, column=1, pady=5, sticky="we")
        lblApellido = Label(self.FrmNvoPaciente, text="Apellido: ")
        lblApellido.grid(row=1, column=0, sticky="e", pady=5, padx=1)
        txtApellido = Entry(self.FrmNvoPaciente, textvariable=self.apellido)
        txtApellido.grid(row=1, column=1, pady=5, sticky="we")
        lblMail = Label(self.FrmNvoPaciente, text="Correo: ")
        lblMail.grid(row=2, column=0, sticky="e", pady=5, padx=1)
        txtMail = Entry(self.FrmNvoPaciente, textvariable=self.email)
        txtMail.grid(row=2, column=1, pady=5, sticky="we")
        lblTel = Label(self.FrmNvoPaciente, text="Telefono: ")
        lblTel.grid(row=3, column=0, sticky="e", pady=5, padx=1)
        txtTel = Entry(self.FrmNvoPaciente, textvariable=self.telefono)
        txtTel.grid(row=3, column=1, pady=5, sticky="we")
        lblComentarios = Label(self.FrmNvoPaciente, text="Notas: ")
        lblComentarios.grid(row=4, column=0, sticky="e", pady=5, padx=1)
        txtComentarios = Text(self.FrmNvoPaciente, height=10, width=40)
        txtComentarios.grid(row=4, column=1, columnspan=3, sticky="nsew", pady=5, padx=1)
        scllVNvoPaciente = Scrollbar(self.FrmNvoPaciente, command=txtComentarios.yview)
        scllVNvoPaciente.grid(row=4, column=4, sticky="nsew")
        txtComentarios.config(yscrollcommand=scllVNvoPaciente.set)
        btnGuardar = ttk.Button(self.FrmNvoPaciente, text="Guardar", command=lambda: self.nuevoPaciente(txtComentarios.get("1.0", 'end-1c')))
        btnGuardar.grid(row=5, column=0, sticky="e")
        btnSalir = ttk.Button(self.FrmNvoPaciente, text='Cerrar', command=lambda: self.cerrarDialogo(self.dlgNvoPaciente))
        btnSalir.grid(row=5, column=1, sticky="w")
        def habilitarModificacion():
            if (self.habilitado == 0):
                self.FrmNvoPaciente.config(text="Modificar Paciente")
                txtNombre.config(state='normal')
                txtApellido.config(state='normal')
                txtMail.config(state='normal')
                txtTel.config(state='normal')
                txtComentarios.config(state='normal')
                btnGuardar.config(state='normal')
                btnEliminarPaciente.config(state='enabled')
                btnModificarPacientes.config(state='enabled')
                btnModificarPacientes.config(text="Visualizar")
                self.habilitado = 1
            else:
                self.FrmNvoPaciente.config(text="Visualizar Paciente")
                txtNombre.config(state='disabled')
                txtApellido.config(state='disabled')
                txtMail.config(state='disabled')
                txtTel.config(state='disabled')
                txtComentarios.config(state='disabled')
                btnGuardar.config(state='disabled')
                btnEliminarPaciente.config(state='disabled')
                btnModificarPacientes.config(text="Modificar")
                self.habilitado = 0
        if (kargs):
            paciente_sel = self.buscarPaciente(3, str(kargs[0]))[0]  
            self.nombre.set(paciente_sel[1])
            self.apellido.set(paciente_sel[2])
            self.email.set(paciente_sel[3])
            self.telefono.set(paciente_sel[4])
            txtComentarios.insert("insert", paciente_sel[5])
            #Cambio el titulo del frame
            self.FrmNvoPaciente.config(text="Visualizar Paciente")
            #Boton Eliminar Paciente
            btnEliminarPaciente = ttk.Button(self.FrmNvoPaciente, text='Eliminar paciente', command=lambda: self.eliminarPaciente(paciente_sel[0]))
            btnEliminarPaciente.grid(row=5, column=3, sticky="ew")
            #Boton habilitar modificacion
            btnModificarPacientes = ttk.Button(self.FrmNvoPaciente, text='Modificar', command=habilitarModificacion)
            btnModificarPacientes.grid(row=5, column=2, sticky="ew")
            #Boton para enviar los cambios a la base
            btnGuardar = ttk.Button(self.FrmNvoPaciente, text="Guardar", command=lambda: self.modificarPacientes(paciente_sel[0], txtComentarios.get("1.0", 'end-1c')))
            btnGuardar.grid(row=5, column=0, sticky="e")
            txtNombre.config(state='disabled')
            txtApellido.config(state='disabled')
            txtMail.config(state='disabled')
            txtTel.config(state='disabled')
            txtComentarios.config(state='disabled')
            btnGuardar.config(state='disabled')
            btnEliminarPaciente.config(state='disabled')

    def ifazSesiones(self):
        idPacienteSel = self.treePaciente.focus()
        if (idPacienteSel != ""):
            #Ocultamos la ventanaPrincipal mientras esta el dialogo abierto
            self.ventanaPrincipal.withdraw()
            pacienteSel = self.pacientes.consulta("SELECT * FROM pacientes WHERE id_paciente="+idPacienteSel)
            self.dlgIfzSesiones = Toplevel()
            #Hacemos que el protocolo de cierre de dialogo llame al metodo CerrarDialogo
            self.dlgIfzSesiones.protocol("WM_DELETE_WINDOW", lambda: self.cerrarDialogo(self.dlgIfzSesiones))
            self.dlgIfzSesiones.resizable(0, 0)
            self.FrmifazSesiones = ttk.LabelFrame(self.dlgIfzSesiones, text="Sesiones del paciente - "+pacienteSel[0][1]+" "+pacienteSel[0][2])
            self.FrmifazSesiones.pack(expand=True, fill=BOTH)
            #Lista de Sesiones
            self.treeifazSesiones = ttk.Treeview(self.FrmifazSesiones,selectmode='browse')
            self.treeifazSesiones.grid(row=1, column=0, columnspan=4)
            self.treeifazSesiones["columns"] = ("1", "2", "3")
            self.treeifazSesiones.column("#0", width=100, minwidth=10, stretch=NO)
            self.treeifazSesiones.column("1", width=100, minwidth=150, stretch=NO)
            self.treeifazSesiones.column("2", width=100, minwidth=150)
            self.treeifazSesiones.column("3", width=350, minwidth=150, stretch=NO)
            self.treeifazSesiones.heading("#0", text="Fecha", anchor=W)
            self.treeifazSesiones.heading("1", text="Hora de inicio", anchor=W)
            self.treeifazSesiones.heading("2", text="Hora de finalización", anchor=W)
            self.treeifazSesiones.heading("3", text="Nota", anchor=W)
            self.scllPaciente = ttk.Scrollbar(self.FrmifazSesiones, command=self.treeifazSesiones.yview)
            self.scllPaciente.grid(row=1, column=4, sticky="nsew")
            self.treeifazSesiones.config(yscrollcommand=self.scllPaciente.set)
            btnCerrar = ttk.Button(self.FrmifazSesiones, text='Cerrar', command=lambda: self.cerrarDialogo(self.dlgIfzSesiones))
            btnCerrar.grid(row=5, column=1)
            self.listaSesiones = self.sesiones.consulta("SELECT pacientes.nombre,pacientes.apellido,sesiones.inicio,sesiones.fin,sesiones.notas FROM pacientes INNER JOIN sesiones ON pacientes.id_paciente=sesiones.id_paciente WHERE pacientes.id_paciente="+idPacienteSel+" ORDER BY sesiones.inicio DESC;")
            for entrada in self.treeifazSesiones.get_children():
                self.treeifazSesiones.delete(entrada)
            for sesion in self.listaSesiones:
                self.treeifazSesiones.insert('', 'end', text=sesion[2][6:8]+"/"+sesion[2][4:6]+"/"+sesion[2][0:4], values=(sesion[2][8:],sesion[3][8:],sesion[4]))
        else:
            messagebox.showinfo("Error", "No se seleccionó ningún paciente")
