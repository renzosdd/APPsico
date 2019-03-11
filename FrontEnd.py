from tkinter import *
from tkinter import ttk, messagebox
from tkinter import scrolledtext as st
from tkinter.ttk import *
import sys
from sys import platform as _platform
import platform
import BackEnd as B
from tkcalendar import Calendar, DateEntry
from datetime import datetime,time,date

if _platform == 'darwin':
    import locale
    if locale.getlocale()[0] is None:
        locale.setlocale(locale.LC_ALL,'es_UY.UTF-8')
elif _platform == 'win32':
    print("win")

print(_platform)
class IfazPrincipal:
    def __init__(self, ifazLogin,usuario):
        self.ventanaPrincipal = Toplevel(ifazLogin)
        self.ventanaPrincipal.title("APPSico - El Bosque")
        self.ventanaPrincipal.iconbitmap('APPsico.ico')
        self.ventanaPrincipal.resizable(0, 0)
        self.ventanaPrincipal.protocol("WM_DELETE_WINDOW", lambda: self.cerrarDialogo(self.ventanaPrincipal,ifazLogin))
        self.pacientes = B.Paciente()
        self.sesiones=B.Sesion()
        self.usuario=usuario
        self.ventanas = 0
        self.frmIfazPrincipal = ttk.LabelFrame(self.ventanaPrincipal, text="Pacientes")
        self.frmIfazPrincipal.pack(expand=True, fill=BOTH)
        self.busqueda=StringVar()
        #Campo de busqueda
        self.txtBuscarPaciente = Entry(self.frmIfazPrincipal,textvariable=self.busqueda)
        if _platform == "linux" or _platform == "linux2" or _platform == "win32" or _platform == "win64":
            self.txtBuscarPaciente.bind('<Button-3>',clickDerecho, add='')
        elif _platform == "darwin":
            self.txtBuscarPaciente.bind('<Button-2>',clickDerecho, add='')
        self.txtBuscarPaciente.grid(row=0, column=0, pady=5, padx=1, sticky="ew")
        self.txtBuscarPaciente.config(width=45)
        #Boton Buscar
        self.btnBuscarPaciente = ttk.Button(self.frmIfazPrincipal, text="Buscar", command=lambda: self.buscarPaciente(1))
        self.btnBuscarPaciente.grid(row=0, column=1, pady=5, padx=1, sticky="nsew")
        #Boton Refrescar
        self.btnRefrescarPacientes = ttk.Button(self.frmIfazPrincipal, text="Reestablecer", command=lambda: self.buscarPaciente(2))
        self.btnRefrescarPacientes.grid(row=0, column=2, pady=5, padx=1, sticky="nsew")
        ttk.Button(self.frmIfazPrincipal, text="Cerrar Sesion", command=lambda:self.cerrarDialogo(self.ventanaPrincipal,ifazLogin)).grid(row=0,column=3, pady=5, padx=1, sticky="nsew")
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
        #Boton para abrir interfaz sesiones
        self.btnifazSesiones = ttk.Button(self.frmIfazPrincipal, text='Sesiones', command=self.ifazSesiones)
        self.btnifazSesiones.grid(row=2, column=0, sticky="ew")
        #Refrescamos lista de pacientes
        self.buscarPaciente(2)
        #Inicializamos el menu contextual
        self.menu()

    #Menu contextual para TreePacientes
    def menu(self):
        self.aMenu = Menu(self.frmIfazPrincipal, tearoff=0)
        if _platform == "linux" or _platform == "linux2" or _platform == "win32" or _platform == "win64":
            self.treePaciente.bind('<Button-3>', self.popup)
        elif _platform == "darwin":
            self.treePaciente.bind('<Button-2>', self.popup)
        self.aMenu.add_command(label='Sesiones', command=self.ifazSesiones)
        self.aMenu.add_command(label='Ficha del paciente', command=self.visualizarPacientes)

    def popup(self, event):
        if self.treePaciente.focus():
            self.aMenu.post(event.x_root, event.y_root)
            self.tree_item = self.treePaciente.focus()

    def buscarPaciente(self, modo, *kwarg):
        #Modo busqueda
        if modo == 1:
            busqueda = self.busqueda.get()
            listapacientes = self.pacientes.consulta("SELECT * FROM pacientes WHERE nombre LIKE '%"+busqueda+"%' OR apellido LIKE '%"+busqueda+"%' OR mail LIKE '%"+busqueda+"%' AND usuario='"+self.usuario+"'")
        #Modo para encontrar a todos los pacientes
        elif modo == 2:
            listapacientes = self.pacientes.consulta("SELECT * FROM pacientes WHERE usuario='"+self.usuario+"'")
            self.busqueda.set("")
        #Busqueda de paciente pasando un ID
        elif modo == 3 and kwarg:
            id_sel = str(kwarg[0])
            paciente_sel = self.pacientes.consulta("SELECT * FROM pacientes WHERE id_paciente = '"+id_sel+"' AND usuario='"+self.usuario+"'")
            return paciente_sel
        for entrada in self.treePaciente.get_children():
            self.treePaciente.delete(entrada)
        for paciente in listapacientes:
            self.treePaciente.insert('', 'end', text=paciente[1], values=(paciente[2], paciente[3], paciente[4]), iid=paciente[0])

    def nuevoPaciente(self, txtComentarios):
        try:
            self.pacientes.alta(self.nombre.get(), self.apellido.get(), self.email.get(), self.telefono.get(), txtComentarios, self.usuario)
            messagebox.showinfo("Se creo correctamente", "El paciente " +self.nombre.get()+" "+self.apellido.get()+" fue creado correctamente")
            self.cerrarDialogo(self.dlgNvoPaciente,self.ventanaPrincipal)
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
            self.pacientes.modificar(str(id_paciente), self.nombre.get(), self.apellido.get(), self.email.get(), self.telefono.get(), txtComentarios)
            messagebox.showinfo("Se Modifico correctamente", "El paciente " +self.nombre.get()+" "+self.apellido.get()+" se modifico correctamente")
            self.buscarPaciente(2)
            self.cerrarDialogo(self.dlgNvoPaciente,self.ventanaPrincipal)
        except:
            messagebox.showinfo("Error al crear el paciente", "No se pudo crear")

    def eliminarPaciente(self, id_paciente):
        resultado = messagebox.askquestion("Eliminar", "¿Esta seguro que desea eliminar al paciente?", icon='warning')
        if resultado == 'yes':
            try:
                self.pacientes.baja(str(id_paciente))
                messagebox.showinfo("Éxito","Se elimino correctamente")
                self.buscarPaciente(2)
                self.cerrarDialogo(self.dlgNvoPaciente,self.ventanaPrincipal)
            except:
                messagebox.showinfo("Error","No se pudo eliminar")
        else:
            pass

    def cerrarDialogo(self,dialogo,parent):
        dialogo.destroy()
        self.ventanas=0
        parent.state(newstate='normal')
        parent.deiconify()

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
        self.dlgNvoPaciente.protocol("WM_DELETE_WINDOW", lambda: self.cerrarDialogo(self.dlgNvoPaciente,self.ventanaPrincipal))
        self.dlgNvoPaciente.resizable(0,0)
        self.dlgNvoPaciente.iconbitmap('APPsico.ico')
        self.FrmNvoPaciente = ttk.LabelFrame(self.dlgNvoPaciente, text="Alta paciente")
        self.FrmNvoPaciente.pack(expand=True, fill=BOTH)
        lblNombre = Label(self.FrmNvoPaciente, text="Nombre: ")
        lblNombre.grid(row=0, column=0, sticky="e", pady=5, padx=1)
        txtNombre = Entry(self.FrmNvoPaciente, textvariable=self.nombre)
        txtNombre.bind('<Button-3>',clickDerecho, add='')
        txtNombre.grid(row=0, column=1, pady=5, sticky="we")
        lblApellido = Label(self.FrmNvoPaciente, text="Apellido: ")
        lblApellido.grid(row=1, column=0, sticky="e", pady=5, padx=1)
        txtApellido = Entry(self.FrmNvoPaciente, textvariable=self.apellido)
        txtApellido.bind('<Button-3>',clickDerecho, add='')
        txtApellido.grid(row=1, column=1, pady=5, sticky="we")
        lblMail = Label(self.FrmNvoPaciente, text="Correo: ")
        lblMail.grid(row=2, column=0, sticky="e", pady=5, padx=1)
        txtMail = Entry(self.FrmNvoPaciente, textvariable=self.email)
        txtMail.bind('<Button-3>',clickDerecho, add='')
        txtMail.grid(row=2, column=1, pady=5, sticky="we")
        lblTel = Label(self.FrmNvoPaciente, text="Telefono: ")
        lblTel.grid(row=3, column=0, sticky="e", pady=5, padx=1)
        txtTel = Entry(self.FrmNvoPaciente, textvariable=self.telefono)
        txtTel.bind('<Button-3>',clickDerecho, add='')
        txtTel.grid(row=3, column=1, pady=5, sticky="we")
        lblComentarios = Label(self.FrmNvoPaciente, text="Notas: ")
        lblComentarios.grid(row=4, column=0, sticky="e", pady=5, padx=1)
        txtComentarios = st.ScrolledText(self.FrmNvoPaciente, height=10, width=40)
        txtComentarios.bind('<Button-3>',clickDerecho, add='')
        txtComentarios.grid(row=4, column=1, columnspan=3, sticky="nsew", pady=5, padx=1)
        btnGuardar = ttk.Button(self.FrmNvoPaciente, text="Guardar", command=lambda: self.nuevoPaciente(txtComentarios.get("1.0", 'end-1c')))
        btnGuardar.grid(row=5, column=0, sticky="e")
        btnSalir = ttk.Button(self.FrmNvoPaciente, text='Cerrar', command=lambda: self.cerrarDialogo(self.dlgNvoPaciente,self.ventanaPrincipal))
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
            btnGuardar.config(command=lambda: self.modificarPacientes(paciente_sel[0], txtComentarios.get("1.0", 'end-1c')))
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
            self.dlgIfzSesiones.protocol("WM_DELETE_WINDOW", lambda: self.cerrarDialogo(self.dlgIfzSesiones,self.ventanaPrincipal))
            self.dlgIfzSesiones.resizable(0, 0)
            self.dlgIfzSesiones.iconbitmap('APPsico.ico')
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
            self.scllSesiones = ttk.Scrollbar(self.FrmifazSesiones, command=self.treeifazSesiones.yview)
            self.scllSesiones.grid(row=1, column=4, sticky="nsew")
            self.treeifazSesiones.config(yscrollcommand=self.scllSesiones.set)
            btnNuevaSesion=ttk.Button(self.FrmifazSesiones,text='Nueva Sesion',command=lambda:self.ifazSesion(idPacienteSel) )
            btnNuevaSesion.grid(row=5, column=0, sticky="ew")
            btnVisualizarSesion=ttk.Button(self.FrmifazSesiones,text='Visualizar Sesion',command=lambda:self.ifazSesion(idPacienteSel,self.treeifazSesiones.focus()) )
            btnVisualizarSesion.grid(row=5, column=1, sticky="ew")
            btnCerrar = ttk.Button(self.FrmifazSesiones, text='Cerrar', command=lambda: self.cerrarDialogo(self.dlgIfzSesiones,self.ventanaPrincipal))
            btnCerrar.grid(row=5, column=3, sticky="ew")
            self.recargarSesiones(idPacienteSel)
        else:
            messagebox.showinfo("Error", "No se seleccionó ningún paciente")

    def recargarSesiones(self,idPacienteSel):
            self.listaSesiones = self.sesiones.consulta("SELECT pacientes.nombre,pacientes.apellido,sesiones.inicio,sesiones.fin,sesiones.notas,sesiones.id_sesion FROM pacientes INNER JOIN sesiones ON pacientes.id_paciente=sesiones.id_paciente WHERE pacientes.id_paciente="+idPacienteSel+" ORDER BY sesiones.inicio DESC;")
            for entrada in self.treeifazSesiones.get_children():
                self.treeifazSesiones.delete(entrada)
            for sesion in self.listaSesiones:
                self.treeifazSesiones.insert('', 'end', text=sesion[2][8:10]+"-"+sesion[2][5:7]+"-"+sesion[2][0:4], values=(sesion[2][11:],sesion[3][11:],sesion[4]), iid=sesion[5])

    def nuevaSesion(self, fechainicio,horainicio, minutosinicio, fechafin, horafin, minutosfin, notas, idPacienteSel):
        try:
            Hinicio=time(int(horainicio),int(minutosinicio))
            Hfin=time(int(horafin),int(minutosfin))
            FHinicio=str(fechainicio) + " " + str(Hinicio)
            FHfin=str(fechafin) + " " + str(Hfin)
            self.sesiones.alta(str(notas),FHinicio,FHfin,str(idPacienteSel))
            self.recargarSesiones(idPacienteSel)
            self.cerrarDialogo(self.dlgIfazSesion,self.dlgIfzSesiones)
        except:
            messagebox.showerror("Error","No se pudo crear")

    def modificarSesion(self, fechainicio,horainicio, minutosinicio, fechafin, horafin, minutosfin, notas, idSesionSel,idPacienteSel):
        try:
            Hinicio=time(int(horainicio),int(minutosinicio))
            Hfin=time(int(horafin),int(minutosfin))
            FHinicio=str(fechainicio) + " " + str(Hinicio)
            FHfin=str(fechafin) + " " + str(Hfin)
            self.sesiones.modificar(str(idSesionSel),notas,FHinicio,FHfin)
            self.recargarSesiones(idPacienteSel)
            self.cerrarDialogo(self.dlgIfazSesion,self.dlgIfzSesiones)
        except:
            messagebox.showinfo("Error al modificar el paciente", "No se pudo modificar")

    def eliminarSesion(self,idSesionSel,idPacienteSel):
        resultado = messagebox.askquestion("Eliminar", "¿Esta seguro que desea eliminar la sesión?", icon='warning')
        if resultado == 'yes':
            try:
                self.sesiones.baja(str(idSesionSel))
                messagebox.showinfo("Éxito","Se elimino correctamente")
                self.recargarSesiones(idPacienteSel)
                self.cerrarDialogo(self.dlgIfazSesion,self.dlgIfzSesiones)
            except:
                messagebox.showinfo("Error","No se pudo eliminar")
        else:
            pass

    def ifazSesion(self, idPacienteSel, *kargs):
        #Comprobamos si se seleccionó alguna sesion
        if (kargs and kargs[0]==''):
            messagebox.showinfo("Error", "No se seleccionó ningúna sesion")
            return
        self.habilitado = 0
        #Ocultamos la ventanaPrincipal mientras esta el dialogo abierto
        self.dlgIfzSesiones.withdraw()
        #Creamos una ventana
        self.dlgIfazSesion = Toplevel()
        #Hacemos que el protocolo de cierre de dialogo llame al metodo CerrarDialogo
        self.dlgIfazSesion.protocol("WM_DELETE_WINDOW", lambda: self.cerrarDialogo(self.dlgIfazSesion,self.dlgIfzSesiones))
        self.dlgIfazSesion.resizable(0,0)
        self.dlgIfazSesion.iconbitmap('APPsico.ico')
        self.FrmIfazSesion = ttk.LabelFrame(self.dlgIfazSesion, text="Nueva Sesion")
        self.FrmIfazSesion.pack(expand=True, fill=BOTH)

        ttk.Label(self.FrmIfazSesion, text='Inicio: ').grid(row=0,column=0, pady=5, padx=1, sticky="e")
        fechaInicio = DateEntry(self.FrmIfazSesion, width=12, background='green',foreground='white', borderwidth=2, locale='es_UY')
        fechaInicio.grid(row=0,column=1, pady=5, padx=1)

        spinboxHoraInicio=ttk.Spinbox(self.FrmIfazSesion, from_=00, to=23, width=5)
        spinboxHoraInicio.grid(row=0, column=2, pady=5, padx=1, sticky="w")
        ttk.Label(self.FrmIfazSesion, text=":").grid(row=0,column=2, pady=5, padx=1)
        spinboxMinInicio=ttk.Spinbox(self.FrmIfazSesion, from_=00, to=59, width=5)
        spinboxMinInicio.grid(row=0, column=2, pady=5, padx=1, sticky="e")
        ttk.Label(self.FrmIfazSesion, text='Fin: ').grid(row=1,column=0, pady=5, padx=1, sticky="e")
        fechaFin = DateEntry(self.FrmIfazSesion, width=12, background='green',foreground='white', borderwidth=2, locale='es_UY')
        fechaFin.grid(row=1,column=1, pady=5, padx=1)
        spinboxHoraFin=ttk.Spinbox(self.FrmIfazSesion, from_=00, to=23, width=5)
        spinboxHoraFin.grid(row=1, column=2, pady=5, padx=1, sticky="w")
        ttk.Label(self.FrmIfazSesion, text=":").grid(row=1,column=2, pady=5, padx=1)
        spinboxMinFin=ttk.Spinbox(self.FrmIfazSesion, from_=00, to=59, width=5)
        spinboxMinFin.grid(row=1, column=2, pady=5, padx=1, sticky="e")

        lblComentarios = Label(self.FrmIfazSesion, text="Notas: ")
        lblComentarios.grid(row=2, column=0, pady=5, padx=1, sticky="e")
        txtComentarios = st.ScrolledText(self.FrmIfazSesion, height=15, width=60)
        txtComentarios.bind('<Button-3>',clickDerecho, add='')
        txtComentarios.grid(row=2, column=1, columnspan=4, sticky="nsew", pady=5, padx=1)

        btnGuardar = ttk.Button(self.FrmIfazSesion, text="Guardar",command=lambda: self.nuevaSesion(fechaInicio.get_date(),spinboxHoraInicio.get(), spinboxMinInicio.get(), fechaFin.get_date(), spinboxHoraFin.get(), spinboxMinFin.get(),txtComentarios.get("1.0", 'end-1c'),idPacienteSel))
        btnGuardar.grid(row=5, column=0, sticky="e")
        btnSalir = ttk.Button(self.FrmIfazSesion, text='Cerrar', command=lambda: self.cerrarDialogo(self.dlgIfazSesion,self.dlgIfzSesiones))
        btnSalir.grid(row=5, column=1, sticky="w")
        def habilitarModificacion():
            if (self.habilitado == 0):
                self.FrmIfazSesion.config(text="Modificar Sesion")
                spinboxHoraFin.config(state='normal')
                spinboxMinFin.config(state='normal')
                spinboxHoraInicio.config(state='normal')
                spinboxMinInicio.config(state='normal')
                fechaInicio.config(state='normal')
                fechaFin.config(state='normal')
                txtComentarios.config(state='normal')
                btnGuardar.config(state='normal')
                btnEliminarSesion.config(state='enabled')
                btnModificarSesion.config(state='enabled')
                btnModificarSesion.config(text="Visualizar")
                self.habilitado = 1
            else:
                self.FrmIfazSesion.config(text="Visualizar Sesion")
                spinboxHoraFin.config(state='disabled')
                spinboxMinFin.config(state='disabled')
                spinboxHoraInicio.config(state='disabled')
                spinboxMinInicio.config(state='disabled')
                fechaInicio.config(state='disabled')
                fechaFin.config(state='disabled')
                txtComentarios.config(state='disabled')
                btnGuardar.config(state='disabled')
                btnEliminarSesion.config(state='disabled')
                btnModificarSesion.config(text="Modificar")
                self.habilitado = 0
        if(kargs):
            idSesionSel=kargs[0]
            sesion_sel = B.query("SELECT * FROM sesiones WHERE id_sesion='"+str(idSesionSel)+"';").fetchall()[0]  
            fInicio=date(int(sesion_sel[2][0:4]),int(sesion_sel[2][5:7]),int(sesion_sel[2][8:10]))
            fFin=date(int(sesion_sel[3][0:4]),int(sesion_sel[3][5:7]),int(sesion_sel[3][8:10]))
            spinboxHoraFin.set(int(sesion_sel[3][11:13]))
            spinboxMinFin.set(int(sesion_sel[3][14:16]))
            spinboxHoraInicio.set(int(sesion_sel[2][11:13]))
            spinboxMinInicio.set(int(sesion_sel[2][14:16]))
            fechaInicio.set_date(fInicio)
            fechaFin.set_date(fFin)
            txtComentarios.insert("insert", sesion_sel[1])
            #Cambio el titulo del frame
            self.FrmIfazSesion.config(text="Visualizar Sesion")
            spinboxHoraFin.config(state='disabled')
            spinboxMinFin.config(state='disabled')
            spinboxHoraInicio.config(state='disabled')
            spinboxMinInicio.config(state='disabled')
            fechaInicio.config(state='disabled')
            fechaFin.config(state='disabled')
            txtComentarios.config(state='disabled')
            btnGuardar.config(state='disabled')
            #Boton Eliminar Paciente
            btnEliminarSesion = ttk.Button(self.FrmIfazSesion, text='Eliminar Sesion',command=lambda: self.eliminarSesion(idSesionSel,idPacienteSel))
            btnEliminarSesion.grid(row=5, column=3, sticky="ew")
            btnEliminarSesion.config(state='disabled')
            #Boton habilitar modificacion
            btnModificarSesion = ttk.Button(self.FrmIfazSesion, text='Modificar', command=habilitarModificacion)
            btnModificarSesion.grid(row=5, column=2, sticky="ew")
            #para modificar el boton guardar
            btnGuardar.config(command=lambda: self.modificarSesion(fechaInicio.get_date(),spinboxHoraInicio.get(), spinboxMinInicio.get(), fechaFin.get_date(), spinboxHoraFin.get(), spinboxMinFin.get(),txtComentarios.get("1.0", 'end-1c'),idSesionSel,idPacienteSel))
            btnGuardar.config(state='disabled')

def clickDerecho(e):
    try:
        def copiar(e, apnd=0):
            e.widget.event_generate('<Control-c>')
        def cortar(e):
            e.widget.event_generate('<Control-x>')
        def pegar(e):
            e.widget.event_generate('<Control-v>')
        e.widget.focus()
        nclst=[
               (' Cortar', lambda e=e: cortar(e)),
               (' Copiar', lambda e=e: copiar(e)),
               (' Pegar', lambda e=e: pegar(e)),
               ]
        rmenu = Menu(None, tearoff=0, takefocus=0)
        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)
        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")
    except:
        pass
    return

def menuClickDerecho(r):
    try:
        if _platform == "linux" or _platform == "linux2" or _platform == "win32" or _platform == "win64":
            for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
                r.bind_class(b, sequence='<Button-3>', func=clickDerecho, add='')
        elif _platform == "darwin":
            for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
                r.bind_class(b, sequence='<Button-2>', func=clickDerecho, add='')
    except:
        pass

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
        
        self.txtUsuario = ttk.Entry(self.raiz, textvariable=self.usuario, width=30)
        self.txtClave = ttk.Entry(self.raiz, textvariable=self.clave, width=30, show="*")
        self.separador = ttk.Separator(self.raiz, orient=HORIZONTAL)
        self.btnAceptar = ttk.Button(self.raiz, text="Aceptar", command=self.aceptar)
        self.btnCancelar = ttk.Button(self.raiz, text="Cancelar", command=quit)
                               
        self.lblUsuario.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.txtUsuario.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
        self.lblClave.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.txtClave.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
        self.separador.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.btnAceptar.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        self.btnCancelar.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)

        self.txtUsuario.focus_set()
        self.raiz.mainloop()
    
    def aceptar(self):
        try:
            listaUsuarios=B.query("SELECT * FROM usuarios WHERE usuario='"+self.usuario.get().lower()+"'").fetchall()
            if(listaUsuarios[0][1] == self.clave.get()):
                self.raiz.withdraw()
                IfazPrincipal(self.raiz,self.usuario.get().lower())
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
