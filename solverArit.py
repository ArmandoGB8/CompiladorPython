from tipo_token import TipoToken
from tokeen import Token
from nodo import Nodo
import tablasimbolos as ts
import sys

class SolverAritmetico:
    def __init__(self ) -> None:
        
        pass


    def resolver(self, n: Nodo):
        if n.hijos is None:
            if n.value.type == TipoToken.NUMBER or n.value.type == TipoToken.STRING:
                return n.value.literal
            
            elif n.value.type == TipoToken.ID:
                return ts.simbolos.obtener(n.value.lexeme)
            else:
                return None
            
            
        nizq:Nodo = n.hijos[0]
        nder:Nodo = n.hijos[1]


        rizquierdo = self.resolver(nizq)
        rderecho = self.resolver(nder)

        if isinstance(rizquierdo,float) and isinstance(rderecho,float):
            match n.value.type:
                case TipoToken.ADD:
                    return rizquierdo + rderecho
                case TipoToken.SUB:
                    return rizquierdo - rderecho
                case TipoToken.MULT:
                    return rizquierdo * rderecho
                case TipoToken.DIAG:
                    return rizquierdo / rderecho
        elif isinstance(rizquierdo,str) and isinstance(rderecho,str):
            if n.value.type == TipoToken.ADD:
                return rizquierdo+rderecho
        else:
            print(F"Error: No se puede resolver la operacion {n.value.type} con las instancias {type(rizquierdo)} y {type(rderecho)}")
        return None
            

    
