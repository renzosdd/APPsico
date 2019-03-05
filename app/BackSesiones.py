import Base as B

class Sesion:

    def __init__(self):
        pass

    def consulta(self, sql):
        row = B.query(sql).fetchall()
        return row
