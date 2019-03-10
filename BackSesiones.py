import Base as B

class Sesion:

    def __init__(self):
        pass

    def alta(self, notas, inicio, fin, id_paciente):
        try:
            B.query('INSERT INTO sesiones (notas, inicio, fin, id_paciente) VALUES ("'+notas+'","'+inicio+'","'+fin+'","'+id_paciente+'");')
        except:
            pass



    def consulta(self, sql):
        row = B.query(sql).fetchall()
        return row
