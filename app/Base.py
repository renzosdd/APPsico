import sqlite3

#Metodo para crear la conexion a la base de datos
def query(sql):
    con = sqlite3.connect('app/APPSico.db')
    with con:
        cur = con.cursor()
        cur.execute(sql)
        return cur
