import Base as B

class Paciente:
    def __init__(self):
        pass

    def alta(self, nombre, apellido, email, tel, notas):
        try:
            B.query('INSERT INTO pacientes (nombre,apellido,mail,telefono,notas) VALUES ("'+nombre+'","'+apellido+'","'+email+'","'+tel+'","'+notas+'");')
            B.close()
        except:
            pass

    def baja(self, id_paciente):
        try:
            B.query('DELETE FROM pacientes WHERE id_paciente = '+id_paciente+';')
            B.close()
        except:
            pass

    def modificar(self, id_paciente, nombre, apellido, email, tel, notas):
        try:
            B.query("UPDATE pacientes SET nombre='"+nombre+"',apellido='"+apellido+"',mail='"+email+"',telefono='"+tel+"',notas='"+notas+"' WHERE id_paciente="+id_paciente+";")
            B.close()
        except:
            pass

    def consulta(self, sql):
        row = B.query(sql).fetchall()
        return row
