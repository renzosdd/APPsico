import tkinter as tk
from tkinter import ttk
from sys import platform as _platform

def clickDerecho(e):
    try:
        def copiar(e, apnd=0):
            e.widget.event_generate('<Control-c>')

        def cortar(e):
            e.widget.event_generate('<Control-x>')

        def pegar(e):
            e.widget.event_generate('<Control-v>')

        e.widget.focus()

        nclst=[
               (' Cortar', lambda e=e: cortar(e)),
               (' Copiar', lambda e=e: copiar(e)),
               (' Pegar', lambda e=e: pegar(e)),
               ]

        rmenu = tk.Menu(None, tearoff=0, takefocus=0)

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")

    except:
        print('Algo Salio mal')
        pass

    return "break"


def menuClickDerecho(r):

    try:
        if _platform == "linux" or _platform == "linux2" or _platform == "win32" or _platform == "win64":
            for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
                r.bind_class(b, sequence='<Button-3>', func=clickDerecho, add='')
        elif _platform == "darwin":
            for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
                r.bind_class(b, sequence='<Button-2>', func=clickDerecho, add='')
    except:
        print (' - menuClickDerecho, something wrong')
        pass
