from tipo_token import TipoToken
from tokeen import Token

class Nodo:
    def __init__(self, value: Token) -> None:
        self.value = value
        self.hijos:list[Nodo] = None
        pass

    def insertar_hijo(self, n):
        if self.hijos is None:
            self.hijos = []
            self.hijos.append(n)
        else:
            self.hijos.insert(0,n)

    def insertar_sig_hijo(self,n):
        if self.hijos is None:
            self.hijos = []
            self.hijos.append(n)
        else:
            self.hijos.append(n)

    def insertar_hijos(self,nodosHijos):
        if self.hijos is None:
            self.hijos = []
        self.hijos.extend(nodosHijos)

