from tkinter import*

master=Tk()
master.title("Ingreso")

def validate1():
    if  entry.get()=="1234":
        label1=Label(master, text="Bienvenido a APPSico")
        label1.grid(row=0,column=3)
        entry.destroy()
        button.destroy()
        label.destroy()
    else:
        label2=Label(master, text="Contraseña incorrecta", background="red", fg="white")
        label2.grid(row=0,column=3)

label=Label(master, text="Ingrese su contraseña: ")
label.grid(row=0,column=0)
           
entry=Entry(master)
entry.grid(row=0,column=1)

button=Button(master, text="Enviar",command=validate1)
button.grid(row=0,column=2)

master.mainloop()