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

class pacientes:
    def __init__(self):
        pass

    #Metodo para definir nuevos pacientes
    def nuevo(self,nombre,apellido,email,tel,notas):
        self.nombre=nombre
        self.apellido=apellido
        self.email=email
        self.tel=tel
        self.notas=notas
        try:
            query('INSERT INTO pacientes (nombre,apellido,mail,telefono,notas) VALUES ("'+self.nombre+'","'+self.apellido+'","'+self.email+'","'+self.tel+'","'+self.notas+'");')
        except:
            pass
            
    #Metodo para consultar pacientes pasandole la sentencia SQL
    def consulta(self,sql):
        row=query(sql).fetchall()
        return row

paciente1=pacientes()
#paciente1.nuevo("prueba","es","prueba@es.es","099999999","esunanotamas")
listapacientes = paciente1.consulta("SELECT * FROM pacientes")
for paciente in listapacientes:
    print(paciente[1])

