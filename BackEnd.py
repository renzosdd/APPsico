import sqlite3

con = sqlite3.connect('APPSico.db')

def query(sql):
        with con:
                cur = con.cursor()
                cur.execute(sql)
                return cur

def close():
        con.close()


class Paciente:
    def __init__(self):
        pass

    def alta(self, nombre, apellido, email, tel, notas, usuario):
        try:
            query('INSERT INTO pacientes (nombre,apellido,mail,telefono,notas,usuario) VALUES ("'+nombre+'","'+apellido+'","'+email+'","'+tel+'","'+notas+'","'+usuario+'");')
        except:
            pass

    def baja(self, id_paciente):
        try:
            query('DELETE FROM pacientes WHERE id_paciente = '+id_paciente+';')
        except:
            pass

    def modificar(self, id_paciente, nombre, apellido, email, tel, notas):
        try:
            query("UPDATE pacientes SET nombre='"+nombre+"',apellido='"+apellido+"',mail='"+email+"',telefono='"+tel+"',notas='"+notas+"' WHERE id_paciente="+id_paciente+";")
        except:
            pass

    def consulta(self, sql):
        row = query(sql).fetchall()
        return row

class Sesion:

    def __init__(self):
        pass

    def alta(self, notas, inicio, fin, id_paciente):
        try:
            query('INSERT INTO sesiones (notas, inicio, fin, id_paciente) VALUES ("'+notas+'","'+inicio+'","'+fin+'","'+id_paciente+'");')
        except:
            pass

    def modificar(self, id_sesion, notas, inicio, fin):
        try:
            query("UPDATE sesiones SET notas='"+notas+"',inicio='"+inicio+"',fin='"+fin+"' WHERE id_sesion="+id_sesion+";")
        except:
            pass

    def baja(self, id_sesion):
        try:
            query('DELETE FROM sesiones WHERE id_sesion = '+id_sesion+';')
        except:
            pass

    def consulta(self, sql):
        row = query(sql).fetchall()
        return row

#sesion=Sesion()
#sesion.modificar("4","Nota Modificada","20190221 2:30:00 PM","20190224 3:55:00 PM")
#sesion.baja("10")
#sesion.alta("Es una nota nueva","20190221 2:30:00 PM","20190224 3:55:00 PM","63")
#for sesion in sesion.consulta("SELECT * FROM sesiones"):
#    print(sesion)
