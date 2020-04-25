from lista_enlazada import *
import soundPlayer as pysounds
import csv

# Constantes de representación
CHR_CANT_TRACKS = "C"
CHR_TRACK = "S"
CHR_TIME = "T"
CHR_MARK = "N"
F_SQUARE = "SQ"
F_TRIA = "TRIA"
F_SINE = "SINE"
F_NOISE = "NOIS"
F_SILENCE = "SILE"

class Cancion:
    '''
    Permite modelar canciones a partir de los sonidos
    de las estructuras de datos contenidas en
    soundPlayer.py y lista_enlazada.py.
    '''

    def __init__(self):
        '''
        Constructor de la clase. Inicializa una canción
        vacia (sin tracks, ni marks, con el cursor en
        la posición inicial y con un iterador de marcas
        vacío).
        '''
        self.tracks = ListaEnlazada()
        self.marks = ListaEnlazada()
        self.cursor = 0


    def clear(self):
        '''
        Vuelve al estado inicial todos los atributos del
        objeto de referencia (vuelve a inicar la instancia
        actual).
        '''
        self.__init__()


    def getTracks(self):
        '''
        Devuelve la lista enlazada de tracks de la canción.
        '''
        return self.tracks
        

    def setTrack(self, frecuencia, volumen, funcion, duty_cycle=0.5):
        '''
        Recibe una frecuencia (número decimal), un nivel
        de volúmen (número del 0 al 1), un tipo de función soportada
        por la SoundFactory de la clase soundPlayer, y opcionalmente un
        duty_cycle (número del 0 al 1 para customizar los sonidos de
        función cuadrada), siendo su valor por defecto 0.5.

        Agrega a los tracks de la canción un sonido en base a los
        parmatros recibidos, creándolo a traves de la SoundFactory
        de la clase soundPlayer.

        Si el tipo de función no esta soportada, levanta la excepción
        ValueError.
        '''
        if duty_cycle>=1 or duty_cycle<0:
            raise ValueError("Duty cycle debe ser menor a 1.")
        
        funcion=funcion.upper()

        if (funcion == F_SINE):
            self.tracks.append([(funcion, frecuencia, volumen) , pysounds.SoundFactory.get_sine_sound(frecuencia, volumen)])
                
        elif (funcion == F_SQUARE):
            self.tracks.append([(funcion, frecuencia, volumen, duty_cycle) , pysounds.SoundFactory.get_square_sound(frecuencia, volumen, duty_cycle)])
                
        elif (funcion == F_TRIA):
            self.tracks.append([(funcion, frecuencia, volumen) , pysounds.SoundFactory.get_triangular_sound(frecuencia, volumen)])
                
        elif (funcion == F_NOISE):
            self.tracks.append([(funcion, frecuencia, volumen) , pysounds.SoundFactory.get_noise_sound(frecuencia, volumen)])
                
        elif (funcion == F_SILENCE):
            self.tracks.append([(funcion, frecuencia, volumen) , pysounds.SoundFactory.get_silence_sound(frecuencia, volumen)])
        
        else:
            raise ValueError("Función no sportada")


    def delTrack(self, pos):
        '''
        Recibe una posición de la lista de tracks (de 1 a n) y quita el
        track de dicha posición de la lista. Todos los tracks posteriores
        al track borrado se mueven un lugar hacia atras para que
        no quede un espacio vacío en la lista.

        Si el track está en uso, se elimina de todos los marks que lo
        utilicen y actualiza las posiciones de las marcas de tiempo
        a los tracks.
        '''
        try:
            pos = int(pos)-1
            if pos<0 :
                raise ValueError
        except ValueError:
            raise ValueError("Posición inválida")
        
        try:
            self.tracks.pop(pos)

            self.actualizarMarks(pos)
        except IndexError:
            raise IndexError("Posición fuera de rango.")
        

    def actualizarMarks(self, inx_track):
        '''
        Recibe un índice de track eliminado, y actualiza las
        referencias de las marcas de tiempo para que continuén
        apuntando a los tracks correctos (eliminando la referencia
        del track borrador).
        '''

        nro_track = inx_track + 1
        # Se guarda aparte el nuevo estado de la lista.        
        marks_next = ListaEnlazada()

        for mark in self.marks:
            tiempo, notas = mark
            tmp_lst = ListaEnlazada()
            new_notas = ListaEnlazada()
            
            for nota in notas:
                if nota > nro_track:
                    new_notas.append(nota-1)
                elif nota < nro_track:
                    new_notas.append(nota)
                    
            tmp_lst.append(tiempo)    
            tmp_lst.append(new_notas)
            marks_next.append(tmp_lst)

        # Se actualiza el estado de la lista.
        self.marks = ListaEnlazada()
        for mark in marks_next:
            self.marks.append(mark)


    def addMark(self, tempo, posicion):
        '''
        Recibe un valor de tiempo (número de segundos) y una posición
        (número que corresponde a la posición en una lista, de 1 a n)
        e intenta agregar una marca de tiempo con la cantidad de segundos
        especificada en la posición parametrizada.

        Si la posición es inválida, levanta la excepción IndexError.
        Si en la posición indicada ya existe una marca de tiempo,
        levanta la excepción ValuError.
        '''
        try:
            tempo = float(tempo)
            if tempo<0:
                raise ValueError
        except ValueError:
            raise ValueError

        marca = ListaEnlazada()
        marca.append(tempo)
        marca.append(ListaEnlazada())

        mark_actual = None

        if len(self.marks)>0:
            mark_actual = self.marks[self.cursor]
            
        self.marks.insert(posicion, marca)
        
        if mark_actual:
            self.cursor = self.marks.index(mark_actual)
            

    def getMarks(self):
        '''
         Devuelve la lista de marcas de tiempo.
        '''
        return self.marks


    def setTrackHere(self, pos):
        '''
        Recibe el número de track a agregar dentro de la marca de tiempo
        actual (según el cursor).

        Si la posición del track es inválida, levanta la excepción ValueError.
        Si la posición ya existe en la marca de tiempo o  esta fuera de rango,
        se levanta la excepción IndexError.
        '''
        # La lista de sonidos siempre está en la posición 1.
        try:
            pos = int(pos)
        except ValueError:
            raise ValueError(pos)
        
        if self.checkTrackPos(pos) and self.checkMarksPos(self.cursor):
            if not self.marks[self.cursor][1].contiene(pos):
                self.marks[self.cursor][1].append(pos)
        else:
            raise IndexError


    def delTrackHere(self, pos):
        '''
        Recibe el número de track a eliminar dentro de la marca de tiempo
        actual (según el cursor).

        Si la posición del track es inválida, levanta la excepción
        ValueError. Si la posición no existe en la marca de tiempo o
        esta fuera de rango, se levanta la excepción IndexError.
        '''
        # La lista de sonidos siempre está en la posición 1.
        try:
            pos = int(pos)
        except ValueError:
            raise ValueError(pos)
        
        if self.checkTrackPos(pos) and self.checkMarksPos(self.cursor):
            if self.marks[self.cursor][1].contiene(pos):
                self.marks[self.cursor][1].remove(pos)
        else:
            raise IndexError


    def checkTrackPos(self, pos):
        '''
        Recibe un número de track y devuelve "True" si es una posición
        de track válida o "False" si no lo es, considerando una posición
        de 1 en adelante.
        '''
        pos = int(pos)
            
        if (pos<=0 or pos>len(self.tracks)):
            return False

        return True


    def checkMarksPos(self, pos):
        '''
        Recibe un número de mark y devuelve "True" si es una posición
        de track válida o "False" si no lo es, considerando los índices
        reales de la lista de marcas.
        '''
        pos = int(pos)
            
        if (pos<0 or pos>=len(self.marks)):
            return False

        return True


    def getPosActual(self):
        '''
        Devuelve la posición actual del cursor.
        '''
        return self.cursor


    def moveCursor(self, valor, haciaAdelante):
        '''
        Recibe un valor, y un indicador booleano si
        que representa si el traslado es hacia adelante.

        Mueve el cursor la cantidad de posiciones
        indicadas por el valor en la lista.

        Si el valor es inválido (no representable como entero),
        no se levanta ninguna excepción, el cursor queda inalterado
        y avisa por pantalla el error.

        Si no hay suficientes marcas hacia adelante, el cursor
        queda al final.

        Si no suficientes marcas hacia atras, el cursor se queda al
        inicio.
        '''
        try:

            if (haciaAdelante):
                valor = int(valor)
            else:
                valor = int('-' + str(valor))

            # Se toma a cero como la primer posción
            prim_pos = 0

            # Se le resta 1 para que su valor
            # se corresponda con el del índice máximo.
            ult_pos = len(self.marks) -1
            pos_futura = self.cursor + valor

            if (pos_futura<0):
                self.cursor = prim_pos
            elif pos_futura>ult_pos:
                self.cursor = ult_pos
            else:
                self.cursor = pos_futura
                
        except ValueError:
            raise ValueError("El valor de traslado no es válido.")


    def fileToSong(self, archivo, con_track):  
        """
        Recibe la ruta de un archivo plp, y la constante de representación para la
        reproducción de un track (char o string que indica que hay que reproducir
        un track específico según el orden de los tracks).

        Si el archivo no pudo cargarse por algún motivo, lanza la excepción IOError.
        """

        try:
            with open(archivo) as f:
                
                tiempo = 0
                primer_mark = True
            
                archivo_csv=csv.reader(f)
                for datos in archivo_csv:
                    field, value=datos
                    
                    if (field == CHR_TRACK):
                        sonido=value.split("|")

                        frecuencia = float(sonido[1])
                        volumen = float(sonido[2])
                        if volumen<0 or volumen>1 or frecuencia<0:
                            raise ValueError

                        #if "SQ" in sonido[0] and len(sonido[0])==4: Caso particular sonido cuadrado
                        funcion = sonido[0][:2]

                        if (funcion == F_SQUARE):
                            duty_cycle = int(sonido[0][2:])/100
                            self.setTrack(frecuencia, volumen, funcion, duty_cycle)
                        else:
                            funcion = sonido[0]
                            self.setTrack(frecuencia, volumen, funcion)
                    
                    elif (field == CHR_TIME):
                        tiempo = value
                    
                    elif (field == CHR_MARK):
                            
                        if primer_mark==False:
                            self.addMark(tiempo, self.getPosActual()+1)
                            self.moveCursor(1, True)
                        else:
                            primer_mark=False
                            self.addMark(tiempo, self.getPosActual())
                            
                        for n_char in range(self.tracks.len):
                            if (value[n_char] == con_track):
                                self.setTrackHere(n_char+1)
                            n_char +=1
                            
                self.cursor = 0
                
        except (IOError, ValueError, IndexError):
            raise IOError("El archivo solicitado no pudo ser cargado.")
        
    
    def songToFile(self, nombre_arch, con_track, sin_track):
        """
        Recibe la ruta de un archivo plp, la constante de representación para la
        reproducción de un track y la constante de representación para
        evitar la reproducción de un track (chars o strings que indican 
        que hay que reproducir un track específico segun el orde de los tracks).

        Si el archivo no pudo guardarse, lanza la excepción IOError.
        """

        try:
            with open(nombre_arch, "w", newline='') as file:
                archivo_csv=csv.writer(file)
                archivo_csv.writerow((CHR_CANT_TRACKS,  str(len(self.tracks))))
                
                #Tracks
                for track in self.tracks:
                    funcion = str(track[0][0])
                    frecuencia = str(track[0][1])
                    vol = str(track[0][2])
                    
                    if F_SQUARE == funcion:
                            duty_call = int(track[0][3]*100)
                            duty_call = str(duty_call)
                            funcion = funcion + duty_call
                            
                    archivo_csv.writerow((CHR_TRACK , "|".join((funcion, frecuencia, vol)) ))
                
                #Tiempo inicial
                if (self.marks):
                    tempo_act=self.marks[0][0]
                    archivo_csv.writerow((CHR_TIME, str(tempo_act)))

                #Notas
                for mark in self.marks:
                    acorde=""

                    #Tiempos diferentes al inicial
                    nro_mark = self.marks.index(mark)
                    if mark[0]!=tempo_act:
                        tempo_act=mark[0]
                        archivo_csv.writerow((CHR_TIME, str(tempo_act)))
                        
                    for nro in range(1, len(self.tracks) + 1):
                        # Las notas a tocar siempre estan en la posición 1 del track
                        if nro in mark[1]:
                            acorde+=con_track
                        else:
                            acorde+=sin_track
                            
                    archivo_csv.writerow((CHR_MARK, acorde))
                    
        except IOError:
            raise IOError("No se pudo guardar el archivo con el nombre especificado.")


    def play(self):
        """
        Reproduce la canción completa.
        """
        if self.tracks.len==0:
            return
        
        pos_notas=ListaEnlazada()
        
        for i in range(len(self.marks)):
            pos_notas.append(i)
        try:
            self.playThis(pos_notas)
        except OSError:
            raise OSError("Ocurrió un problema en la reproducción.")


    def playSeconds(self, n_sec):
        """
        Recibe la cantiad de segundos a reproducir desde la posición
        actual y los reproduce.

        Si la cantidad de segundos parametrizada no es un número
         válido, se lanza la excepción ValueError.
        """

        duracion = 0
        acordes = ListaEnlazada()
        reproductor = pysounds.SoundPlayer(len(self.tracks))
        
        try:
            duracion = float(n_sec)
        except ValueError:
            raise ValueError("Parámetros inválidos.")

        for pos in range(self.cursor, len(self.marks)):
            tiempo, notas = self.marks[pos]
            duracion -= tiempo
            if duracion>=0:
                self.notasALista(tiempo, notas, acordes)
            else:
                residual = duracion + tiempo
                self.notasALista(residual, notas, acordes)
                break

        try:
            for track,tiempo in acordes:
                reproductor.play_sounds(track,tiempo)
        
        except OSError:
            raise OSError("Ocurrió un problema en la reproducción.")


    def playMarks(self, numero):
        """
        Reproduce el número de marcas parametrizado a partir
        de la posición actual del cursor.

        Si el parámetro no es un número, se levanta la
        excepción ValueError.
        """
        n_marcas = 0
        posiciones=ListaEnlazada()
        
        try:
            n_marcas = int(numero)
            if n_marcas <= 0:
                raise ValueError
        except ValueError:
            raise ValueError("Número inválido de marcas.")

        # Se les suma uno a las posiciones de las
        # marcaS límite porque no se incluye al cursor
        mark_max = self.cursor + int(n_marcas)
        mark_min = self.cursor + 1

        if mark_max > len(self.marks)-1:
            raise ValueError("No se puede reproducir esa cantidad de marcas.")

        try:
            # Para que incluya al límite, se le suma uno en el range.
            for nro in range(mark_min, mark_max+1):
                posiciones.append(nro)

            self.playThis(posiciones)
            
        except OSError:
            raise OSError("Ocurrió un problema en la reproducción.")


    def playThis(self, posiciones):
        """
        Recibe una lista de posiciones, y reproduce las marcas
        que se encuentran en las mismas.
        """
        if self.tracks.len==0:
            return
            
        acordes=ListaEnlazada()
        tracks = ListaEnlazada()
        tiempos = ListaEnlazada()
        reproductor = pysounds.SoundPlayer(len(self.tracks))
        
        for pos in posiciones:
            tiempo, notas=self.marks[pos]
            self.notasALista(tiempo, notas, acordes)

        try:
            for track,tiempo in acordes:
                reproductor.play_sounds(track,tiempo)
        
        except OSError:
            raise OSError("Ocurrió un problema en la reproducción.")

    
    def notasALista(self, tiempo, notas, acordes):
        """
        Recibe el tiempo y las notas a reproducir, y 
        agrega el sonido correspondiente a la lista que se pasa por
        parámetro.
        """
        sonidos = ListaEnlazada()
        # Se guardan los sonidos en una nueva lista para una reproducción óptima
        pos = 0
        for n_nota in notas:
            sonidos.append(self.getTracks()[int(n_nota)-1][1])
            pos+=1
        acordes.append((sonidos, tiempo))

