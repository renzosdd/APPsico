# Repo para el proyecto APPsico - ElBosque - BIT

## Pasos para configurar el entorno:


1 - Instalar VSCode (https://code.visualstudio.com/)
Configurar cambiar terminal predeterminada a cmd agregando en user settings (CTRL +SHIFT + P -> Open User Settings):
```
{
    "terminal.integrated.shell.windows": "cmd.exe"
        // otras configuraciones...
}
```
2 - Instalar Github desktop (https://desktop.github.com/)
    - Clonar el proyecto https://github.com/renzosdd/APPsico
    - Click en Abrir en Visual Studio Code
3 - Instalar Python 3.7.2 (https://www.python.org/)
  
## Dependencias del proyecto:
    
1 - tkcalendar (pip install tkcalendar)

##### Dependencias Win 7, 8, 8.1 (64bit)

1 - Para que funcione en estos sistemas es necesario instalar:

    https://support.microsoft.com/es-es/help/2999226/update-for-universal-c-runtime-in-windows

##### Para generar ejecutable

1 - Instalar pyinstaller (pip install pyinstaller)

2 - ejecutar comando desde consola estando posicionado en la carpeta del proyecto:

```
pyinstaller --hidden-import=sys --hidden-import=smtplib --hidden-import=datetime --hidden-import=email.message --hidden-import=re --hidden-import=tkcalendar --hidden-import=tkinter --windowed --noconsole --onefile --icon=./APPsico.ico FrontEnd.py
```

3 - Copiar los archivos APPsico.png, APPsico.ico y APPsico.bd a la carpeta dist
