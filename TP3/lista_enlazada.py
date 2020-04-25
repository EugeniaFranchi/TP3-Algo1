from pila import Pila

class _Nodo:
    """
    Modela los componentes para una estructura, tal que
    cada componente contiene una referencia al siguiente.
    """
    
    def __init__(self, dato=None, prox=None):
        """
        Inicializa la clase Nodo.
        """
        self.dato = dato
        self.prox = prox


    def __str__(self):
        """
        Devuelve la representación "informal" (de cara al usuario)
        de un nodo: el dato que guarda este en formato de cadena.
        """
        return str(self.dato)


    def __repr__(self):
        """
        Devuelve la representación "formal" de un nodo
        (de cara a quien analiza el código): el dato que
        guarda este en formato de cadena seguido del dato
        que guarda el próximo nodo en la cadena.
        """
        try: 
            #return str(self.dato) + "|" + str(self.prox)
            return str(self.dato)
        except AttributeError:
            return "None"
        

    def __eq__(self, nodo):
        """
        Recibe un nodo y lo compara con el actual.

        Si el dato y sucesivo del nodo parmatrizado son iguales
        a los correspondientes del nodo de referencia (el actual, o self)
        entonces devuelve True.

        De lo contrario, devuelve False.
        """

        return (self.dato == nodo.dato) and (self.prox == nodo.prox)
    

######################################################################################


class ListaEnlazada:
    """
    Modela una lista que permite agregar y eliminar
    elementos en tiempo constante.
    """

    def __init__(self):
        """
        Inicializa la lista enlazada, vacía.
        """
        self.primero = None
        self.len = 0
        self.ultimo = None


    def __len__(self):
        """
        Devuelve la longitud de la lista.
        """
        return self.len


    def __iter__(self):
        """
        Devuelve una instancia del iterador correspondiente
        a ListaEnlazada (objeto de la clase _IteradorListaEnlazada),
        que permite recorrela desde el primer elemento.
        """
        return _IteradorListaEnlazada(self.primero)
    

    def __str__(self):
        """
        Devuelve una lista de cadenas de caracteres
        que representan los datos guardados por la lista
        enlazada.
        """
  
        datos = []

        e_actual = self.primero
        
        while e_actual:
            datos.append(e_actual.dato)
            e_actual = e_actual.prox

        return str(datos)


    def __repr__(self):
        """
        Devuelve la representación "formal" de la lista
        enlazada (de cara a quien analiza el código):
        una lista de las representaciones formales de
        cada nodo en la lista enlazada.
        """

        try:
            datos = []
            
            e_actual = self.primero
        
            while e_actual:
                datos.append(repr(e_actual))
                e_actual = e_actual.prox
            return str(datos)
                
        except AttributeError:
            return "[]"


    def contiene(self, dato):
        """
        Recibe un elemento. Devuelve True si el elemento
        está en la lista o false si no lo esta.
        """
        actual = self.primero
        
        while actual:
            if (dato == actual.dato):
                return True
            actual = actual.prox
            
        return False


    def append(self, dato):
        """
        Recibe un valor para agregar a la lista, y
        se agrega un nodo con ese valor al final
        de la misma.
        """
        
        nuevo = _Nodo(dato)
        
        if not self.len:
            self.primero = nuevo
        
        else:
            ante_ultimo = self.ultimo
            ante_ultimo.prox = nuevo
        
        self.ultimo = nuevo
        self.len+=1


    def insert(self, p, dato):
        """
        Inserta el elemento "dato" en la posición "p"
        (ambos parámetros).
        Si la posición es inválida, levanta IndexError.
        """

        pos = 0
        
        pos=self.validar_posicion(p)
        
        nuevo = _Nodo(dato)

        if (pos == 0):
            nuevo.prox = self.primero
            self.primero = nuevo
            
        else:    
            anterior = self.primero
            for i in range(1, pos):
                anterior = anterior.prox
                
            if (pos == self.len):
                anterior.prox=nuevo
                self.ultimo=nuevo
            else:
                nuevo.prox = anterior.prox
                anterior.prox = nuevo

        self.len += 1


    def validar_posicion(self, p):
        """
        Recibe una posición y la devuelve como entero. Levanta una 
        excepción en caso de que la posición no sea válida.
        """
        try:
            pos  = int(p)
        except ValueError:
            raise ValueError("No es un número entero")
        
        if (pos < 0) or (pos > self.len):
            raise IndexError("Posición inválida.")
        return(pos)


    def pop(self, p=None):
        """
        Elimina el nodo de la posición pasada por parámetro, y
        devuelve el dato que contenia el nodo.
        
        Si la posición no corresponde a la lista, se levanta la excepción
        IndexError. Si no se recibe la posición, elimina el último nodo.
        """

        ult_pos = self.len-1

        if p == None:
            p = ult_pos

        pos = 0
        
        pos=self.validar_posicion(p)
        
        
        if (pos == 0):
            dato = self.primero.dato
            self.primero = self.primero.prox
            if self.len == 1:
                self.ultimo = None

        elif (pos == ult_pos):
            dato = self.ultimo.dato
            actual = self.primero
            
            for i in range(1, pos):
                actual = actual.prox
                
            self.ultimo = actual
            self.ultimo.prox = None
                  
        else:
            anterior = self.primero
            actual = anterior.prox
            for i in range(1, pos):
                anterior = actual
                actual = anterior.prox

            dato = actual.dato
            anterior.prox = actual.prox

        self.len-=1
        return dato


    def remove(self, x):
        """
        Borra la primera aparición del valor parametrizado en la lista.
        Si el valor pasado por parametro no está en la lista, levanta
        la excepción ValueError.
        """
        
        if (self.len == 0):
            raise ValueError("Lista vacía")
        
        elif (self.primero.dato == x):
            self.pop(0)

        elif(self.ultimo.dato == x):
            self.pop()

        else:
            anterior = self.primero
            actual = anterior.prox
            
            while actual and (actual.dato != x):
                anterior = actual
                actual = anterior.prox

            if not actual:
                raise ValueError("Elemento inexistente.")

            anterior.prox = actual.prox

            self.len-=1


    def index(self, e):
        """		
	Recibe un dato y devuelve el índice en la lista del
	primer elemento que contenga ese dato.
	"""
        actual = self.primero
        indice = 0
        
        while actual and (actual.dato != e):
            indice += 1
            actual = actual.prox
            
        if not actual:
            raise ValueError("Elemento inexistente.")
            
        return indice


    def __getitem__(self, index):
        """
        Devuelve el elemento de la lista cuya posición corresponde
        al índice parametrizado (comportamiento contrario a index).
        """

        index = int(index)
        anterior = self.primero
        actual = anterior
        
        for i in range(1, self.len):
            anterior = actual
            actual = anterior.prox
            if i==index:
                return actual.dato

        if index==0 and self.len:
            return self.primero.dato
        else:
            raise IndexError


######################################################################################
        
      
class _IteradorListaEnlazada:
    """
    Modela el iterador para la clase ListaEnlazada.
    """

    def __init__(self, elemento):
        """
        Inicializa el iterador a partir del nodo
        parametrizado.
        """
        self.actual = elemento
        self.anteriores = Pila()


    def __next__(self):
        """
        Devuelve el próximo elemento de la lista (la información
        del nodo siguiente).

        Si el nodo es el último, termina con la iteración.
        """
        if not self.actual:
            raise StopIteration()

        dato = self.actual.dato
        self.anteriores.apilar(self.actual)
        self.actual = self.actual.prox
        return dato


    def anterior(self):
        """
        Devuelve el anterior elemento de la lista (la información
        del nodo anterior).

        Si el nodo es el primero, termina con la iteración.
        """

        if self.anteriores.esta_vacia():
            raise StopIteration()

        nodo = self.anteriores.desapilar()
        self.actual = nodo
        return nodo.dato
