import sqlite3

#Metodo para crear la conexion a la base de datos
con = sqlite3.connect('app/APPSico.db')

def query(sql):
        with con:
                cur = con.cursor()
                cur.execute(sql)
                return cur

def close():
        con.close()

