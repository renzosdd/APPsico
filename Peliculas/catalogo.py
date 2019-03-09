from io import open
import pickle

class Pelicula:
    
    # Constructor de clase
    def __init__(self, titulo, duracion, lanzamiento):
        self.titulo = titulo
        self.duracion = duracion
        self.lanzamiento = lanzamiento
        print('Se ha creado la película:',self.titulo)
        
    def __str__(self):
        return '{} ({})'.format(self.titulo, self.lanzamiento)


class Catalogo:
    
    peliculas = []
    
    # Constructor de clase
    def __init__(self):
        self.cargar()
        
    def agregar(self,p):
        self.peliculas.append(p)
        self.guardar() #Guardado automatico
        
    def mostrar(self):
        if len(self.peliculas) == 0:
            print("El catalogo esta vacio")
            return

        for p in self.peliculas:
            print(p)
        
    def cargar(self):
        fichero = open('catalogo.pckl','ab+')
        fichero.seek(0)
        try:
            self.peliculas = pickle.load(fichero)
        except:
            print("El fichero esta vacio")
        finally:
            fichero.close()
            del(fichero)
            print("Se han cargado {} peliculas".format(len(self.peliculas)))
    
    def guardar(self):
        fichero = open('catalogo.pckl','wb')
        pickle.dump(self.peliculas,fichero)
        fichero.close()
        del(fichero)

    #Destructor de clase
    def __del__(self):
        self.guardar() #Guardado automatico
        print("se guardo automaticamente el fichero")

c=Catalogo()
c.agregar( Pelicula('El padrino',175,1972) )
#c.agregar( Pelicula('El padrino: parte 2',202,1974) )
c.mostrar()