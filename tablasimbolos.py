import sys

class TSimbolos:
    def __init__(self) -> None:
        self.valores = {}

    def existeIdentificador(self, key) -> bool:
        if key in self.valores.keys():
            return True
        return False
    
    def obtener(self, key):
        if self.existeIdentificador(key):
            return self.valores[key]
        else:
            print(f"Variable {key} no definida")
            sys.exit()
        
    def asignar(self, key, value):
        if self.existeIdentificador(key):
            self.valores[key]=value
            return
        else:
            self.valores.__setitem__(key,value)
            return
        raise Exception(f"Variable {key} no definida")

    def reasig(self, key, value):
        self.valores[key]=value
        return

def init():
    global simbolos
    simbolos = TSimbolos() 
        

