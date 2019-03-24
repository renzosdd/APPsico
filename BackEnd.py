import sqlite3
import smtplib
import email.message

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
        
        server = smtplib.SMTP('smtp.live.com: 587')
        email_content = """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>Demystifying Email Design</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            </head>
            <body style="margin: 0; padding: 0;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%">	
                    <tr>
                        <td style="padding: 10px 0 30px 0;">
                            <table align="center" border="0" cellpadding="0" cellspacing="0" width="500" style="border: 1px solid #cccccc; border-collapse: collapse;">
                                <tr>
                                    <td align="center" bgcolor="#70bbd9" style="font-size: 28px; font-weight: bold; font-family: Arial, sans-serif;">
                                        <img src="https://i.ibb.co/q7qRyx9/APPsico.png" alt="APPsico" width="500" height="300" style="display: block;" />
                                    </td>
                                </tr>
                                <tr>
                                    <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                            <tr>
                                                <td style="color: #153643; font-family: Arial, sans-serif; font-size: 24px;">
                                                    <b>Nueva consulta mediante APPsico</b>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 20px 0 30px 0; color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 15px;">
                                                    Tuvo una consulta con <b>"""+profesional.capitalize()+"""</b>. <br/><br/> Comenzando con fecha y hora: <b>"""+fechaInicio+"""</b> <br/><br/>  Finalizando con fecha y hora:: <b>"""+fechaFin+"""</b>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>
                                                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td bgcolor="#f2eee2" style="padding: 30px 30px 30px 30px;">
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                            <tr>
                                                <td style="color: #afe191; font-family: Arial, sans-serif; font-size: 14px;" width="75%">
                                                    <b>&reg; APPsico - El Bosque</b><br/>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </body>
            </html>
        """
        msg = email.message.Message()
        msg['From'] = "APPsico@outlook.com"
        msg['To'] = destinatario
        msg['Subject'] = "Nueva sesion con "+profesional.capitalize()+" mediante APPsico."

        #Contraseña de aplicacion de Outlook
        password = "jkpwkfjlkavnikzs"
        #Creamos la cabecera y le agregamos el contenido
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)
        #Creamos el servidor (en este caso usando Outlook)
        server = smtplib.SMTP('smtp.live.com: 587')
        server.starttls()
        # Se realiza el login
        server.login(msg['From'], password)
        # Enviamos el mensaje mediante el servidor
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()


