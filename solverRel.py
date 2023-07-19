from tipo_token import TipoToken
from tokeen import Token
from nodo import Nodo
import tablasimbolos as ts
import sys
from postfixgen import Postfix
from solverArit import SolverAritmetico

class SolverRel:
    def __init__(self) -> None:
        self.poshelp = Postfix([])
        pass

    def resolver(self, n:Nodo):

        if n.hijos is None:
            if n.value.type == TipoToken.NUMBER or n.value.type == TipoToken.STRING or n.value.type ==TipoToken.TRUE or n.value.type == TipoToken.FALSE:
                return n.value.literal
            elif n.value.type == TipoToken.ID:
                return ts.simbolos.obtener(n.value.lexeme)


        nizq:Nodo = n.hijos[0]
        nder:Nodo = n.hijos[1]
        
        if self.poshelp.esOperador(nizq.value.type) and self.poshelp.esOperador(nder.value.type):
            sol = SolverAritmetico()
            rizquierdo = sol.resolver(nizq)
            rderecho = sol.resolver(nder)
        elif self.poshelp.esOperador(nizq.value.type):
            rderecho = self.resolver(nder)
            sol = SolverAritmetico()
            rizquierdo = sol.resolver(nizq)
        elif self.poshelp.esOperador(nder.value.type):
            rizquierdo = self.resolver(nizq)
            sol = SolverAritmetico()
            rderecho = sol.resolver(nder)
        else:
            rizquierdo = self.resolver(nizq)
            rderecho = self.resolver(nder)



        if type(rizquierdo) == type(rderecho) and type(rderecho) == float:
            match n.value.type:
                case TipoToken.GREAT:
                    return rizquierdo > rderecho
                case TipoToken.GREAT_EQUAL:
                    return rizquierdo >= rderecho
                case TipoToken.EQUAL:
                    return rizquierdo == rderecho
                case TipoToken.LESS_THAN:
                    return rizquierdo < rderecho
                case TipoToken.LESS_EQUAL:
                    return rizquierdo <= rderecho
                case TipoToken.DIFERENT:
                    return rizquierdo != rderecho
        elif type(rizquierdo) == type(rderecho):
            if n.value.type == TipoToken.EQUAL:
                return rizquierdo == rderecho
            else:
                print(F"Error: No se puede resolver la operacion {str(n.value.type)[10:]} con las instancias {type(rizquierdo)} y {type(rderecho)}")
                sys.exit()
        else:
            print(F"Error: No se puede resolver la operacion {str(n.value.type)[10:]} con las instancias {type(rizquierdo)} y {type(rderecho)}")
            sys.exit()
        return None





        

    
