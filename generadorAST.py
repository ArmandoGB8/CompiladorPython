from tipo_token import TipoToken
from tokeen import Token
from nodo import Nodo
from postfixgen import Postfix
from arbol import Arbol

class GeneradorAST:
    def __init__(self, postfija:list[Token]) -> None:
        self.postfija = postfija
        self.stackk= []
        self.poshelp = Postfix(None)

    def generarAST(self):
        stackPadres = []
        raiz = Nodo(Token(TipoToken.NULL,"","",None))
        stackPadres.append(raiz)

        padre:Nodo = raiz

        for i,t in enumerate(self.postfija):
            if t.type == TipoToken.EOF:
                break
            
            if t.type in self.poshelp.palabras_reservadas.values():
                n = Nodo(t)
                padre = stackPadres[-1]
                padre.insertar_sig_hijo(n)
                stackPadres.append(n)
                padre = n
            elif self.poshelp.esOperando(t.type):
                #print(f"{t.type}")
                n = Nodo(t)
                self.stackk.append(n)
            elif self.poshelp.esOperador(t.type):
                aridad = self.poshelp.obAridad(t.type)
                n = Nodo(t)
                for i in range(aridad):
                    nodoAux = self.stackk.pop()
                    n.insertar_hijo(nodoAux)
                self.stackk.append(n)
            elif t.type == TipoToken.SEMICOLON:
                
                if len(self.stackk) == 0:
                    stackPadres.pop()
                    padre = stackPadres[-1]
                else:
                    n:Nodo = self.stackk.pop()

                    if padre.value.type == TipoToken.VAR:
                        if n.value.type == TipoToken.ASIGNATION:
                            padre.insertar_hijos(n.hijos)
                        else:
                            padre.insertar_sig_hijo(n)
                        stackPadres.pop()
                        padre = stackPadres[-1]
                    elif padre.value.type == TipoToken.PRINT:
                        padre.insertar_sig_hijo(n)
                        stackPadres.pop()
                        padre = stackPadres[-1]
                    else:
                        padre.insertar_sig_hijo(n)

        programa = Arbol(raiz)
        return programa
    
    def printAST(self, nodo:Nodo, nivel=0):
        if nodo is None:
            return
        
        print(f"{' '*nivel}{nodo.value}")
        
        if nodo.hijos:
            for i in nodo.hijos:
                self.printAST(i,nivel+1)
        

                        
            

            



    