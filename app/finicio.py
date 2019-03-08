from tkinter import *

finicio=Tk()
finicio.title("Fecha de Inicio")

label1=Label(finicio, text="Dia")
label1.grid(row=0,column=0)
spinbox_dia=Spinbox(finicio,fg="blue", font=12, from_=1, to=31)
spinbox_dia.grid(row=1, column=0)

label1=Label(finicio, text="Mes")
label1.grid(row=0,column=1)
spinbox_mes=Spinbox(finicio, fg="blue", font=12, values=("Enero","Febrero",
                                       "Marzo", "Abril","Mayo","Junio","Julio","Agosto",
                                      "Setiembre", "Octubre", "Noviembre","Diciembre"))
spinbox_mes.grid(row=1, column=1)

label1=Label(finicio, text="Año")
label1.grid(row=0,column=2)
spinbox_anio=Spinbox(finicio, fg="blue", font=12, from_=2019, to=2099)
spinbox_anio.grid(row=1, column=2)

label1=Label(finicio, text="Hora")
label1.grid(row=0,column=3)
spinbox_hora=Spinbox(finicio, fg="blue", font=12, from_=8, to=21)
spinbox_hora.grid(row=1, column=3)

label1=Label(finicio, text="Minutos")
label1.grid(row=0,column=4)
spinbox_minuto=Spinbox(finicio, fg="blue", font=12, from_=1, to=60)
spinbox_minuto.grid(row=1, column=4)


finicio.mainloop()