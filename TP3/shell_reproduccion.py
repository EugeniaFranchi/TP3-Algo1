import cmd
from os import system
import soundPlayer as pysounds
import csv
from cancion import Cancion
from lista_enlazada import *

CHR_TRACK = '#'
CHR_NO_TRACK = '.'

class ShellReproduccion(cmd.Cmd):
    """
    Implementación particular de la clase cmd (incluída en Python 3.6), con
    especifcaciones en español particulares para el menu de reproducción de
    sonido del Editor PLP.

    Para ver la documentación completa de la clase cmd, buscar su código fuente
    en la carpeta Lib en el directorio de instalación de python.
    """
    intro = '\nEditor PLP - Modo Reproducción.\nIngrese help o ? para listar los comandos.\n'
    doc_header= "Comandos para el modo reproducción del Editor PLP (ingrese help <comando>):"
    misc_header = "Otros temas de ayuda:"
    undoc_header = "Comandos no documentados:"
    nohelp = "*** No hay información sobre %s"
    prompt = '[->] '
    ruler = '='
    comando_vacio = ''

    def iniciar(self):
        """
        Limpia la pantalla y llama a la función cmdloop
	(definida en la clase Cmd) para inicializar el
	shell actual.
        """
        system('cls')
        self.cmdloop()
        
        
    def do_EXIT(self, parametro):
        """
        Limpia la pantalla y vuelve al menú principal.
        """
        system('cls')
        return True
    

    def default(self, line):
        """
        Método sobre-escrito de la clase cmd.
        
        Recibe una línea ingresada por pantalla.
        
        Método llamado al realizar un input que referencia a un comando
        desconocido.

        """
        self.stdout.write('Comando desconocido: %s\n\n'%line)


    def emptyline(self):
        """
        Método sobre-escrito de la clase cmd.

        Se sobre escribe para que no realice ninguna acción en caso
        de que la línea ingresada este vacia (devuelve None).
        
        Método llamado cuando el input por pantalla es una línea vacia.
        """
        return None


    def do_PLAY(self, paramatros):
        """
        Permite ingresar la ruta a un archivo .plp y reproducirlo.
        """
        archivo_c=input("Ingrese ruta del archivo o nombre (si es local):")

        try:
            cancion = Cancion()
            cancion.fileToSong(archivo_c, CHR_TRACK)
            cancion.play()
        except IOError as ioerror:
            print(ioerror)
        except ValueError as valuerror:
            print(valuerror)
        except IndexError as indexerror:
            print(indexerror)
