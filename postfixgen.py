from tokeen import Token
from tipo_token import TipoToken
from tablasimbolos import TSimbolos

class Postfix:
    def __init__(self, tokens) -> None:
        #self.simbolos = simbolos
        self.infija = tokens
        self.stackk = []
        self.postfija = []
        self.palabras_reservadas = {  # Diccionario con las palabras reservadas y su tipo de token correspondiente
            "class": TipoToken.CLASS,
            "also": TipoToken.ALSO,
            "for": TipoToken.FOR,
            "fun": TipoToken.FUN,
            "if": TipoToken.IF,
            "null": TipoToken.NULL,
            "print": TipoToken.PRINT,
            "return": TipoToken.RETURN,
            "super": TipoToken.SUPER,
            "this": TipoToken.THIS,
            "var": TipoToken.VAR,
            "while": TipoToken.WHILE,
            "else": TipoToken.ELSE,
        }

    def convertir(self):
        estructuraDeControl = False
        stack_Estruc:list[Token] = []
        auxfor = 0

        for index,t in enumerate(self.infija):
            if t.type == TipoToken.EOF:
                break
            
            if t.type in self.palabras_reservadas.values():
                self.postfija.append(t)
                if self.esEstructuraDeControl(t.type):
                    estructuraDeControl = True
                    stack_Estruc.append(t)
            elif self.esOperando(t.type):
                self.postfija.append(t)
            elif t.type == TipoToken.PARENT_OPEN:
                self.stackk.append(t)
            elif t.type == TipoToken.PARENT_CLOSE:
                while( ( len(self.stackk) != 0) and (self.stackk[-1].type != TipoToken.PARENT_OPEN) ):
                    temp = self.stackk.pop()
                    self.postfija.append(temp)
                if self.stackk[-1].type == TipoToken.PARENT_OPEN:
                    self.stackk.pop()
                if estructuraDeControl:
                    self.postfija.append(Token(TipoToken.SEMICOLON,";",";",None))
            elif self.esOperador(t.type):
                while len(self.stackk)!=0 and self.precedenciaMayorIgual(self.stackk[-1].type, t.type):
                    temp = self.stackk.pop()
                    self.postfija.append(temp)
                self.stackk.append(t)
            elif t.type == TipoToken.SEMICOLON:
                while len(self.stackk) !=0 and self.stackk[-1].type != TipoToken.BRACKET_OPEN:
                    if estructuraDeControl:
                        if stack_Estruc[-1].type == TipoToken.FOR:
                            temp = self.stackk.pop()
                            self.postfija.append(temp)
                            break
                        pass
                    temp = self.stackk.pop()
                    self.postfija.append(temp)
                self.postfija.append(t) 
            elif t.type == TipoToken.BRACKET_OPEN:
                self.stackk.append(t)
            elif t.type == TipoToken.BRACKET_CLOSE and estructuraDeControl:
                if self.infija[index+1].type == TipoToken.ELSE:
                    self.stackk.pop()
                else:
                    self.stackk.pop()
                    self.postfija.append(Token(TipoToken.SEMICOLON,";",";",None))
                    stack_Estruc.pop()
                    if len(stack_Estruc) == 0:
                        estructuraDeControl = False

        while(len(self.stackk) != 0):
            temp = self.stackk.pop()
            self.postfija.append(temp)

        while( len(stack_Estruc) != 0):
            #print("sem")
            stack_Estruc.pop()
            self.postfija.append(Token(TipoToken.SEMICOLON,";",";",None))


        return self.postfija

    def esOperando(self,tipo:TipoToken):
        match tipo:
            case TipoToken.ID:
                return True
            case TipoToken.NUMBER | TipoToken.STRING | TipoToken.TRUE | TipoToken.FALSE:
                return True
            case other:
                return False

    def esEstructuraDeControl(self,tipo):
        match tipo:
            case TipoToken.IF | TipoToken.ELSE:
                return True
            case TipoToken.WHILE | TipoToken.FOR:
                return True
            case _:
                return False

    def esOperador(self,tipo:TipoToken):
        #print("esop")
        match tipo:
            case TipoToken.ADD | TipoToken.SUB | TipoToken.MULT | TipoToken.DIAG:
                return True
            case TipoToken.EQUAL | TipoToken.DIFERENT | TipoToken.GREAT | TipoToken.GREAT_EQUAL:
                return True
            case TipoToken.AND | TipoToken.OR | TipoToken.ASIGNATION:
                return True
            case TipoToken.LESS_THAN | TipoToken.LESS_EQUAL:
                return True
            case other:
                return False


    def precedenciaMayorIgual(self, tipo1, tipo2):
        return  self.obtenerPrecedencia(tipo1) >= self.obtenerPrecedencia(tipo2)

    def obtenerPrecedencia(self,tipo):
        match tipo:
            case TipoToken.MULT | TipoToken.DIAG:
                return 7 
            case TipoToken.ADD | TipoToken.SUB:
                return 6
            case TipoToken.GREAT_EQUAL | TipoToken.GREAT | TipoToken.LESS_THAN | TipoToken.LESS_EQUAL:
                return 5
            case TipoToken.DIFERENT | TipoToken.EQUAL:
                return 4
            case TipoToken.AND:
                return 3
            case TipoToken.OR:
                return 2
            case TipoToken.ASIGNATION:
                return 1
            case _:
                return 0


    def obAridad(self,tipo: TipoToken):
        match tipo:
            case TipoToken.MULT| TipoToken.DIAG| TipoToken.SUB| TipoToken.ADD| TipoToken.EQUAL| TipoToken.GREAT| TipoToken.GREAT_EQUAL | TipoToken.ASIGNATION:
                return 2
            case TipoToken.LESS_THAN | TipoToken.LESS_EQUAL | TipoToken.DIFERENT | TipoToken.AND | TipoToken.OR :
                return 2
            case other:
                return 0