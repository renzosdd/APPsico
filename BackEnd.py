import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

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
            query("DELETE FROM sesiones WHERE id_sesion = '"+id_sesion+"';")
        except:
            pass

    def consulta(self, sql):
        row = query(sql).fetchall()
        return row

class envioMail:
    def __init__(self,destinatario,profesional,fechaInicio,fechaFin):
        # create message object instance
        msg = MIMEMultipart()
        
        
        message = "Tuvo una sesion con: "+profesional+" inició: "+fechaInicio+" finalizó: "+fechaFin
        # setup the parameters of the message
        password = "gsbuqvkpqwryvhvq"
        msg['From'] = "APPsico@outlook.com"
        msg['To'] = destinatario
        msg['Subject'] = "Nueva sesion con "+profesional
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        #create server
        server = smtplib.SMTP('smtp.live.com: 587')
        
        server.starttls()
        
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        
        
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        
        server.quit()

        #print ("successfully sent email to %s:" % (msg['To']))