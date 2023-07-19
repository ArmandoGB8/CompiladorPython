from tipo_token import TipoToken


class Token:

    def __init__(self, tipo: TipoToken, lexema: str, literal, linea: int) -> None:
        self.type = tipo
        self.lexeme = lexema
        self.literal = literal  
        self.line = linea

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return self.type == other.type

    def __repr__(self) -> str:
        return f"<{self.type}, lexema:{self.lexeme}, literal:{self.literal}, linea:{self.line}>"
