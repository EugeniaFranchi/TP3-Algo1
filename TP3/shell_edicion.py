import cmd
import soundPlayer as pysounds

from os import system
from os import path
from lista_enlazada import *
from cancion import Cancion

cancion = Cancion()
CHR_TRACK = '#'
CHR_NO_TRACK = '.'

class ShellEdicion(cmd.Cmd):
    """
    Implementación particular de la clase cmd (incluída en Python 3.6), con
    especifcaciones en español particulares para el menu de edición de sonido
    del Editor PLP.

    Para ver la documentación completa de la clase cmd, buscar su código fuente
    en la carpeta Lib en el directorio de instalación de python.
    """
   
    intro = '\nEditor PLP - Modo Edición.\nIngrese help o ? para listar los comandos.\n'
    doc_header="Comandos para el modo edición del Editor PLP (ingrese help <comando>):"
    misc_header = "Otros temas de ayuda:"
    undoc_header = "Comandos no documentados:"
    nohelp = "*** No hay información sobre %s"
    prompt = '{->} '
    ruler = '='
    comando_vacio = ''

    # La documentación de las funciones "do_..." están orientadas al usuario.

    def iniciar(self):
        """
        Limpia la pantala y llama a la función
        cmdloop (definida en la clase Cmd) para
        inicializar el shell actual.
        """
        system('cls')
        cancion = Cancion()
        self.cmdloop()


    def do_EXIT(self, parametro):
        """
        Limpia la pantalla y vuelve al menú principal.
        """
        cancion.clear()
        system('cls')
        return True
    
    
    def do_LOAD(self, archivo):
        """
        Permite cargar un archivo .plp
        
        En caso de haber una canción en edición actual, la reemplaza.

        Ejemplo: LOAD cacion.plp
        (cargar el archivo local "cancion.plp",
        en la ruta actual del programa).
        """
        cancion.clear()
        
        try:
            cancion.fileToSong(archivo,CHR_TRACK)
        except IOError as ioerror:
            print(str(ioerror))

    
    def do_STORE(self, parametros):
        """
        Permite guardar la canción actualmente en edición en un
        archivo, con el nombre especificado por parámetro.

        Ejemplo: STORE cancion.plp
        (guarda el archivo en la ruta actual del programa).
        """
        respuesta_ok="si"
        respuesta = respuesta_ok
        
        if path.exists(parametros):
            respuesta=input("¿Desea sobreescribir el archivo? si/no: ")
            
        if respuesta.lower()==respuesta_ok:
            try:
                cancion.songToFile(parametros,CHR_TRACK,CHR_NO_TRACK)
            except IOError as ioerror:
                print(str(ioerror))
        else:
            print("El archivo no se guardó.")
            

    def do_STEP(self, parametros):
        """
        Avanza a la siguiente marca de tiempo.

        Si no hay mas marcas hacia adelante, no hace nada.

        Ejemplo: STEP
        """
        if len(cancion.marks)!=0:
            cancion.moveCursor(1,True)


    def do_BACK(self, parametros):
        """
        Retrocede a la anterior marca de tiempo.

        Si no hay mas marcas hacia atrás, no hace nada.
        """
        cancion.moveCursor(1,False)


    def do_STEPM(self, parametros):
        """
        Avanza N marcas de tiempo hacia adelante.

        Si no hay mas marcas hacia adelante, no hace nada.
        """
        try:
            cancion.moveCursor(parametros, True)
        except ValueError as valuerror:
            print(str(valuerror))


    def do_BACKM(self, parametros):
        """
        Retrocede N marcas de tiempo hacia atrás.

        Si no hay mas marcas hacia atrás, no hace nada.

        Ejemplo: STEPM 6
        """
        try:
            cancion.moveCursor(parametros, False)
        except ValueError as valuerror:
            print(str(valuerror))


    def do_MARKADD(self, parametros):
        """
        Agrega una marca de tiempo de la duración establecida
        (en segundos) en la posición actual.

        Ejemplo: MARKADD 2
        """
        try:
            cancion.addMark(parametros, cancion.getPosActual())
            cancion.moveCursor(1, False)
        except IndexError:
            print("Posición inválida.")
        except ValueError:
            print("Tiempo invalido")


    def do_MARKADDNEXT(self, parametros):
        """
        Agrega una marca de tiempo de la duración establecida
        (en segundos) en la posición siguiente a la del cursor.

        Ejemplo: MARKADDNEXT 2
        """
        try:
            cancion.addMark(parametros, cancion.getPosActual()+1)
        except IndexError:
            print("Posición inválida.")
        except ValueError:
            print("Tiempo invalido.")

    def do_MARKADDPREV(self, parametros):
        """
        Agrega una marca de tiempo de la duración establecida
        (en segundos) en la posición anterior a la del cursor.

        Ejemplo: MARKADDPREV 2
        """        
        try:
            # Siempre la primer posición está en el índice 0
            
            posicion = cancion.getPosActual()
            
            if cancion.getPosActual()==0:
                posicion = 0

            cancion.addMark(parametros, posicion)
        except IndexError:
            print("Posición inválida.")
        except ValueError:
            print("Tiempo invalido o posición inválida.")

    def do_TRACKADD(self, parametros):
        """
        Agrega un track con el sonido indicado.
        Recibe una función, una frecuencia (número decimal)
        y un nivel de volúmen (0 a 1).

        Tipos de funciones soportadas:
        SQ: onda cuadrada
        TRIA: onda triangula
        SINE: onda sinusoidal
        NOIS: sonido de ruido
        SILE: silencio

        Para el duty_cycle (4to parametro de SQ)
        se recibe un número del 0 al 1.

        Si se especifica el tipo de función sin más
        parámetros, se crea un sonido "vacío" (no audible).

        Ejemplo: TRACKADD sine 440 0.2
        """
        funcion = ""
        frecuencia = 0
        volumen = 0
        duty_cycle = 0

        try:
            # Formateo de parametros para crear el sonido	
            parametros = str(parametros)

            valores = parametros.split()
            cant_valores = len(valores)

            if (cant_valores == 3):
                funcion, frecuencia, volumen = valores

            elif (cant_valores == 4):
                funcion, frecuencia, volumen, duty_cycle = valores

            else:
                raise ValueError
            
            funcion = str(funcion).upper()
            frecuencia = float(frecuencia)
            volumen = float(volumen)
            duty_cycle = float(duty_cycle)
            
            if volumen>1 or volumen<0 or frecuencia<0:
                raise ValueError

            # Se pasan los parámetros numéricos a dos decimales            
            "{:.2f}".format(frecuencia)
            "{:.2f}".format(volumen)
            "{:.2f}".format(duty_cycle)

            cancion.setTrack(frecuencia, volumen, funcion, duty_cycle)
    
        except ValueError:
            print("Parametros inválidos. Por favor ver la ayuda de este comando.")


    def do_TRACKDEL(self, parametros):
        """
        Elimina el número de track (1 a n) indicado de la lista de tracks,
        trasladando un lugar hacia atrás todos los tracks posteriores al
        borrado.
        
        Ejemplo: TRACKDEL 2
        """
        try:
            cancion.delTrack(parametros)
        except ValueError as err_valor:
            print(err_valor)
        except IndexError as err_inx:
            print(err_inx)


    def do_TRACKON(self, parametros):
        """
        Habilita al número de track seleccionado en la marca de
        tiempo actual del cursor (las posiciones se consideran
        de 1 en adelante).
        """
        try:
            cancion.setTrackHere(parametros)
        except ValueError:
            print("Posición inválida.")
        except IndexError:
            print("Posición fuera de rango.")

	
    def do_TRACKOFF(self, parametros):
        """
        Deshabilita al número de track seleccionado en la marca de
        tiempo actual del cursor (las posiciones se consideran
        de 1 en adelante).
        """
        try:
            cancion.delTrackHere(parametros)
        except ValueError as err_valor:
            print("Posición inválida.")
        except IndexError as err_inx:
            print("Posición fuera de rango.")


    def do_PLAY(self, parametros):
        """
        Reproduce la marca en la que se encuentra el cursor actualmente.
        """
        try:
            posicion = ListaEnlazada()
            posicion.append(cancion.cursor)
            cancion.playThis(posicion)
        except OSError:
             print(str(os_err))

    
    def do_PLAYALL(self, parametros):
        """
        Reproduce toda la canción.
        """
        try:
            cancion.play()
        except OSError as os_err:
            print(str(os_err))

    
    def do_PLAYMARKS(self, parametros):
        """
        Reproduce las próximas n marcas desde la posición actual del cursor.
        """
        try:
            cancion.playMarks(parametros)
        except ValueError as err_num:
            print(str(err_num))
        except IndexError as err_inx:
            print(str(err_inx))
        except OSError as os_err:
            print(str(os_err))
        
    
    def do_PLAYSECONDS(self, parametros):
        """
        Reproduce los próximos n segundos la posición actual. Si la nota
        actual tiene un tempo menor a los segundos indicados, deja de reproducirse
        cuando su tempo lo indique.
        """
        try:
            cancion.playSeconds(parametros)
        except ValueError as valuerror:
            print(str(valuerror))
        except OSError as os_err:
            print(str(os_err))
            

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