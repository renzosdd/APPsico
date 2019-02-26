import sqlite3 as lite
import sys

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
            print("INSERT INTO pacientes (nombre,apellido,mail,telefono,notas) VALUES ('"+self.nombre+"','"+self.apellido+"','"+self.email+"','"+self.tel+"','"+self.notas+"');")
        except:
            pass

    def baja(self,id_paciente):
        self.id=id_paciente
        try:
            query('DELETE FROM pacientes WHERE id_paciente = '+self.id+';')
        except:
            pass

    def modificar(self,id_paciente,nombre,apellido,email,tel,notas):
        self.id=id_paciente
        self.nombre=nombre
        self.apellido=apellido
        self.email=email
        self.tel=tel
        self.notas=notas
        try:
            query("UPDATE pacientes SET nombre ='"+self.nombre+"',apellido ='"+self.apellido+"',email ='"+self.email+"',telefono ='"+self.tel+"',notas ='"+self.notas+"' WHERE id_paciente='"+self.id+"';")
        except:
            pass
    #Metodo para consultar pacientes pasandole la sentencia SQL
    def consulta(self,sql):
        row=query(sql).fetchall()
        return row

pacientes=Paciente()
pacientes.alta("prueba","es","prueba@es.es","099999999","esunanotamas")
pacientes.modificar("15","aaaaa","es","aaaaa@es.es","099999999","aaaaaaaa")
#pacientes.baja("12")
listapacientes = pacientes.consulta("SELECT * FROM pacientes")
for paciente in listapacientes:
    print(paciente)

    

