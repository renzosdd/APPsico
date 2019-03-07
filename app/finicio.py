from tkinter import *

finicio=Tk()
finicio.title("Fecha de Inicio")

spinbox_dia=Spinbox(finicio,fg="blue", font=12, from_=1, to=31)
spinbox_dia.pack(side=LEFT)

spinbox_mes=Spinbox(finicio, fg="blue", font=12, values=("Enero","Febrero",
                                       "Marzo", "Abril","Mayo","Junio","Julio","Agosto",
                                      "Setiembre", "Octubre", "Noviembre","Diciembre"))
spinbox_mes.pack(side=LEFT)

spinbox_anio=Spinbox(finicio, fg="blue", font=12, from_=2019, to=2099)
spinbox_anio.pack(side=LEFT)

spinbox_hora=Spinbox(finicio, fg="blue", font=12, from_=8, to=21)
spinbox_hora.pack(side=LEFT)

spinbox_minuto=Spinbox(finicio, fg="blue", font=12, from_=1, to=60)
spinbox_minuto.pack(side=LEFT)

finicio.mainloop()