import cmd

from os import system
from shell_edicion import ShellEdicion
from shell_reproduccion import ShellReproduccion

editor = ShellEdicion()
reproductor = ShellReproduccion()

class ShellMenu(cmd.Cmd):
    """
    Implementación particular de la clase cmd (incluída en Python 3.6), con
    especifcaciones en español particulares para el menú del editor PLP.

    Para ver la documentación completa de la clase Cmd, buscar su código fuente
    en la carpeta Lib en el directorio de instalación de python.
    """
    
    intro = '\nEditor PLP.\nIngrese help o ? para listar los comandos.\n'
    doc_header="Comandos para el menú del editor PLP (ingrese help <comando>):"
    misc_header = "Otros temas de ayuda:"
    undoc_header = "Comandos no documentados:"
    nohelp = "*** No hay información sobre %s"
    prompt = '-> '
    ruler = '='
    comando_vacio = ''


    def iniciar(self):
        """
        Limpia la pantala y llama a la función
        cmdloop (definida en la clase Cmd) para
        inicializar el shell actual.
        """
        system('cls')
        self.cmdloop()

    
    def do_EDITAR(self, parametro):
        """
        Ir al modo de edición.
        """
        editor.iniciar()


    def do_REPRODUCIR(self, parametro):
        """
        Ir al modo de reproducción.
        """
        reproductor.iniciar()


    def do_EXIT(self, parametro):
        """
        Cierra el programa.
        """
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

