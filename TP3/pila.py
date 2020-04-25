class Pila:
    """
    Modela una estructura de pila.
    """

    def __init__(self):
        '''
        Inicializa una nueva pila, vacía.
        '''
        self.items = []


    def esta_vacia(self):
        """
        Devuelve True si la pila está vacía, False si no lo está.
        """
        return len(self.items) == 0


    def apilar(self,x):
        """Agrega un elemento al final de la pila."""
        self.items.append(x)


    def desapilar(self):
        """
        Devuelve el elemento tope y lo elimina de la pila.
        Si la pila está vacía levanta una excepción.
        """
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        
        return self.items.pop()
