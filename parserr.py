from typing import List
from tipo_token import TipoToken
from tokeen import Token


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.errors = False
        self.preanalysis = None
        self.i = 0

    def parse(self):
        from interprete import Interprete

        self.preanalysis = self.tokens[self.i]
        self.PROGRAM()

        if not self.errors and not self.preanalysis.type == TipoToken.EOF:
            msg = f"Token inesperado: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)
        elif not self.errors and self.preanalysis.type == TipoToken.EOF:
            #print("Expresion valida")
            pass

    def PROGRAM(self):
        if (
            self.preanalysis.type == TipoToken.CLASS
            or self.preanalysis.type == TipoToken.FUN
            or self.preanalysis.type == TipoToken.VAR
            or self.preanalysis.type == TipoToken.NEGATION
            or self.preanalysis.type == TipoToken.LESS
            or self.preanalysis.type == TipoToken.TRUE
            or self.preanalysis.type == TipoToken.FALSE
            or self.preanalysis.type == TipoToken.NULL
            or self.preanalysis.type == TipoToken.THIS
            or self.preanalysis.type == TipoToken.NUMBER
            or self.preanalysis.type == TipoToken.STRING
            or self.preanalysis.type == TipoToken.ID
            or self.preanalysis.type == TipoToken.PARENT_OPEN
            or self.preanalysis.type == TipoToken.SUPER
            or self.preanalysis.type == TipoToken.FOR
            or self.preanalysis.type == TipoToken.IF
            or self.preanalysis.type == TipoToken.PRINT
            or self.preanalysis.type == TipoToken.RETURN
            or self.preanalysis.type == TipoToken.WHILE
            or self.preanalysis.type == TipoToken.BRACKET_OPEN
        ):
            self.DECLARATION()

    def DECLARATION(self):
        if self.errors:
            return
        if self.preanalysis.type == TipoToken.CLASS:
            self.CLASS_DECL()
            self.DECLARATION()
        elif self.preanalysis.type == TipoToken.FUN:
            self.FUN_DECL()
            self.DECLARATION()
        elif self.preanalysis.type == TipoToken.VAR:
            self.VAR_DECL()
            self.DECLARATION()
        elif (
            self.preanalysis.type == TipoToken.NEGATION
            or self.preanalysis.type == TipoToken.LESS
            or self.preanalysis.type == TipoToken.TRUE
            or self.preanalysis.type == TipoToken.FALSE
            or self.preanalysis.type == TipoToken.NULL
            or self.preanalysis.type == TipoToken.THIS
            or self.preanalysis.type == TipoToken.NUMBER
            or self.preanalysis.type == TipoToken.STRING
            or self.preanalysis.type == TipoToken.ID
            or self.preanalysis.type == TipoToken.PARENT_OPEN
            or self.preanalysis.type == TipoToken.SUPER
            or self.preanalysis.type == TipoToken.FOR
            or self.preanalysis.type == TipoToken.IF
            or self.preanalysis.type == TipoToken.PRINT
            or self.preanalysis.type == TipoToken.RETURN
            or self.preanalysis.type == TipoToken.WHILE
            or self.preanalysis.type == TipoToken.BRACKET_OPEN
            or self.preanalysis.type == TipoToken.GREAT
        ):
            self.STATEMENT()
            self.DECLARATION()

    def CLASS_DECL(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.CLASS:
            self.matchToken(TipoToken.CLASS)
            self.matchToken(TipoToken.ID)
            self.CLASS_INHER()
            self.matchToken(TipoToken.BRACKET_OPEN)
            self.FUNCTIONS()
            self.matchToken(TipoToken.BRACKET_CLOSE)
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def CLASS_INHER(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.LESS_THAN:
            self.matchToken(TipoToken.LESS_THAN)
            self.matchToken(TipoToken.ID)

    def FUN_DECL(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.FUN:
            self.matchToken(TipoToken.FUN)
            self.FUNCTION()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def VAR_DECL(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.VAR:
            self.matchToken(TipoToken.VAR)
            self.matchToken(TipoToken.ID)
            self.VAR_INIT()
            self.matchToken(TipoToken.SEMICOLON)
            self.jump_op()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def VAR_INIT(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.ASIGNATION:
            self.matchToken(TipoToken.ASIGNATION)
            self.EXPRESSION()

    def STATEMENT(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type in [
            TipoToken.NEGATION,
            TipoToken.LESS,
            TipoToken.GREAT,
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
        ]:
            self.EXPR_STMT()
        elif self.preanalysis.type == TipoToken.FOR:
            self.FOR_STMT()
        elif self.preanalysis.type == TipoToken.IF:
            self.IF_STMT()
        elif self.preanalysis.type == TipoToken.PRINT:
            self.PRINT_STMT()
        elif self.preanalysis.type == TipoToken.RETURN:
            self.RETURN_STMT()
        elif self.preanalysis.type == TipoToken.WHILE:
            self.WHILE_STMT()
        elif self.preanalysis.type == TipoToken.BRACKET_OPEN:
            self.BLOCK()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def EXPR_STMT(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type in [
            TipoToken.NEGATION,
            TipoToken.LESS,
            TipoToken.GREAT,
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
        ]:
            self.EXPRESSION()
            self.matchToken(TipoToken.SEMICOLON)
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def FOR_STMT(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.FOR:
            self.matchToken(TipoToken.FOR)
            self.matchToken(TipoToken.PARENT_OPEN)
            self.FOR_STMT_1()
            self.FOR_STMT_2()
            self.FOR_STMT_3()
            self.matchToken(TipoToken.PARENT_CLOSE)
            self.STATEMENT()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def FOR_STMT_1(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.VAR:
            self.VAR_DECL()
        elif self.preanalysis.type in [
            TipoToken.NEGATION,
            TipoToken.LESS,
            TipoToken.GREAT,
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
        ]:
            self.EXPR_STMT()
        elif self.preanalysis.type == TipoToken.SEMICOLON:
            self.matchToken(TipoToken.SEMICOLON)
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def FOR_STMT_2(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type in [
            TipoToken.NEGATION,
            TipoToken.LESS,
            TipoToken.GREAT,
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
        ]:
            self.EXPRESSION()
            self.matchToken(TipoToken.SEMICOLON)
        elif self.preanalysis.type == TipoToken.SEMICOLON:
            self.matchToken(TipoToken.SEMICOLON)
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def FOR_STMT_3(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type in [
            TipoToken.NEGATION,
            TipoToken.LESS,
            TipoToken.GREAT,
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
        ]:
            self.EXPRESSION()

    def IF_STMT(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.IF:
            self.matchToken(TipoToken.IF)
            self.matchToken(TipoToken.PARENT_OPEN)
            self.EXPRESSION()
            self.matchToken(TipoToken.PARENT_CLOSE)
            self.STATEMENT()
            self.ELSE_STATEMENT()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def ELSE_STATEMENT(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.ELSE:
            self.matchToken(TipoToken.ELSE)
            self.STATEMENT()

    def PRINT_STMT(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.PRINT:
            self.matchToken(TipoToken.PRINT)
            self.EXPRESSION()
            self.matchToken(TipoToken.SEMICOLON)
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def RETURN_STMT(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.RETURN:
            self.matchToken(TipoToken.RETURN)
            self.RETURN_EXP_OPC()
            self.matchToken(TipoToken.SEMICOLON)
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def RETURN_EXP_OPC(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type in [
            TipoToken.NEGATION,
            TipoToken.LESS,
            TipoToken.GREAT,
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
        ]:
            self.EXPRESSION()

    def WHILE_STMT(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.WHILE:
            self.matchToken(TipoToken.WHILE)
            self.matchToken(TipoToken.PARENT_OPEN)
            self.EXPRESSION()
            self.matchToken(TipoToken.PARENT_CLOSE)
            self.STATEMENT()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def BLOCK(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.BRACKET_OPEN:
            self.matchToken(TipoToken.BRACKET_OPEN)
            self.BLOCK_DECL()
            self.matchToken(TipoToken.BRACKET_CLOSE)
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def BLOCK_DECL(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type in [
            TipoToken.CLASS,
            TipoToken.FUN,
            TipoToken.VAR,
            TipoToken.NEGATION,
            TipoToken.LESS,
            TipoToken.GREAT,
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
            TipoToken.FOR,
            TipoToken.IF,
            TipoToken.PRINT,
            TipoToken.RETURN,
            TipoToken.WHILE,
            TipoToken.BRACKET_OPEN,
        ]:
            self.DECLARATION()
            self.BLOCK_DECL()

    def EXPRESSION(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type in [
            TipoToken.NEGATION,
            TipoToken.LESS,
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
            TipoToken.GREAT,
        ]:
            self.ASSIGNMENT()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def ASSIGNMENT(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type in [
            TipoToken.NEGATION,
            TipoToken.LESS,
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
            TipoToken.GREAT,
        ]:
            self.LOGIC_OR()
            self.ASSIGNMENT_OPC()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def ASSIGNMENT_OPC(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.ASIGNATION:
            self.matchToken(TipoToken.ASIGNATION)
            self.EXPRESSION()

    def LOGIC_OR(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type in [
            TipoToken.NEGATION,
            TipoToken.LESS,
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
            TipoToken.GREAT,
        ]:
            self.LOGIC_AND()
            self.LOGIC_OR_2()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def LOGIC_OR_2(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.OR:
            self.matchToken(TipoToken.OR)
            self.LOGIC_AND()
            self.LOGIC_OR_2()

    def LOGIC_AND(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type in [
            TipoToken.NEGATION,
            TipoToken.LESS,
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
            TipoToken.GREAT,
        ]:
            self.EQUALITY()
            self.LOGIC_AND_2()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def LOGIC_AND_2(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.AND:
            self.matchToken(TipoToken.AND)
            self.EQUALITY()
            self.LOGIC_AND_2()

    def EQUALITY(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type in [
            TipoToken.NEGATION,
            TipoToken.LESS,
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
            TipoToken.GREAT,
        ]:
            self.COMPARISON()
            self.EQUALITY_2()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def EQUALITY_2(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.DIFERENT:
            self.matchToken(TipoToken.DIFERENT)
            self.COMPARISON()
            self.EQUALITY_2()
        elif self.preanalysis.type == TipoToken.EQUAL:
            self.matchToken(TipoToken.EQUAL)
            self.COMPARISON()
            self.EQUALITY_2()

    def COMPARISON(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type in [
            TipoToken.NEGATION,
            TipoToken.LESS,
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
            TipoToken.GREAT,
        ]:
            self.TERM()
            self.COMPARISON_2()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def COMPARISON_2(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.GREAT_THAN:
            self.matchToken(TipoToken.GREAT_THAN)
            self.TERM()
            self.COMPARISON_2()
        elif self.preanalysis.type == TipoToken.GREAT_EQUAL:
            self.matchToken(TipoToken.GREAT_EQUAL)
            self.TERM()
            self.COMPARISON_2()
        elif self.preanalysis.type == TipoToken.LESS_THAN:
            self.matchToken(TipoToken.LESS_THAN)
            self.TERM()
            self.COMPARISON_2()
        elif self.preanalysis.type == TipoToken.LESS_EQUAL:
            self.matchToken(TipoToken.LESS_EQUAL)
            self.TERM()
            self.COMPARISON_2()

    def TERM(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type in [
            TipoToken.NEGATION,
            TipoToken.LESS,
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
            TipoToken.GREAT,
        ]:
            self.FACTOR()
            self.TERM_2()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def TERM_2(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.LESS:
            self.matchToken(TipoToken.LESS)
            self.FACTOR()
            self.TERM_2()
        elif self.preanalysis.type == TipoToken.ADD:
            self.matchToken(TipoToken.ADD)
            self.FACTOR()
            self.TERM_2()
        elif self.preanalysis.type == TipoToken.SUB:
            self.matchToken(TipoToken.SUB)
            self.FACTOR()
            self.TERM_2()
        elif self.preanalysis.type == TipoToken.GREAT:
            self.matchToken(TipoToken.GREAT)
            self.FACTOR()
            self.TERM_2()

    def FACTOR(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type in [
            TipoToken.NEGATION,
            TipoToken.LESS,
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
            TipoToken.GREAT,
        ]:
            self.UNARY()
            self.FACTOR_2()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def FACTOR_2(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.DIAG:
            self.matchToken(TipoToken.DIAG)
            self.UNARY()
            self.FACTOR_2()
        elif self.preanalysis.type == TipoToken.MULT:
            self.matchToken(TipoToken.MULT)
            self.UNARY()
            self.FACTOR_2()

    def UNARY(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.NEGATION:
            self.matchToken(TipoToken.NEGATION)
            self.UNARY()
        elif self.preanalysis.type == TipoToken.LESS:
            self.matchToken(TipoToken.LESS)
            self.UNARY()
        elif self.preanalysis.type == TipoToken.GREAT:
            self.matchToken(TipoToken.GREAT)
            self.UNARY()
        elif self.preanalysis.type in [
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
        ]:
            self.CALL()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def CALL(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type in [
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
        ]:
            self.PRIMARY()
            self.CALL_2()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def CALL_2(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.PARENT_OPEN:
            self.matchToken(TipoToken.PARENT_OPEN)
            self.ARGUMENTS_OPC()
            self.matchToken(TipoToken.PARENT_CLOSE)
            self.CALL_2()
        elif self.preanalysis.type == TipoToken.DOT:
            self.matchToken(TipoToken.DOT)
            self.matchToken(TipoToken.ID)
            self.CALL_2()

    def PRIMARY(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.TRUE:
            self.matchToken(TipoToken.TRUE)
        elif self.preanalysis.type == TipoToken.FALSE:
            self.matchToken(TipoToken.FALSE)
        elif self.preanalysis.type == TipoToken.NULL:
            self.matchToken(TipoToken.NULL)
        elif self.preanalysis.type == TipoToken.THIS:
            self.matchToken(TipoToken.THIS)
        elif self.preanalysis.type == TipoToken.NUMBER:
            self.matchToken(TipoToken.NUMBER)
        elif self.preanalysis.type == TipoToken.STRING:
            self.matchToken(TipoToken.STRING)
        elif self.preanalysis.type == TipoToken.ID:
            self.matchToken(TipoToken.ID)
        elif self.preanalysis.type == TipoToken.PARENT_OPEN:
            self.matchToken(TipoToken.PARENT_OPEN)
            self.EXPRESSION()
            self.matchToken(TipoToken.PARENT_CLOSE)
        elif self.preanalysis.type == TipoToken.SUPER:
            self.matchToken(TipoToken.SUPER)
            self.matchToken(TipoToken.DOT)
            self.matchToken(TipoToken.ID)
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def FUNCTION(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.ID:
            self.matchToken(TipoToken.ID)
            self.matchToken(TipoToken.PARENT_OPEN)
            self.PARAMETERS_OPC()
            self.matchToken(TipoToken.PARENT_CLOSE)
            self.jump_op()
            self.BLOCK()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def FUNCTIONS(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.ID:
            self.FUNCTION()
            self.FUNCTIONS()

    def PARAMETERS_OPC(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.ID:
            self.PARAMETERS()

    def jump_op(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.jump:
            self.jump_par()

    def jump_par(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.jump:
            self.matchToken(TipoToken.jump)
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def PARAMETERS(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.ID:
            self.matchToken(TipoToken.ID)
            self.PARAMETERS_2()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def PARAMETERS_2(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.COMMA:
            self.matchToken(TipoToken.COMMA)
            self.matchToken(TipoToken.ID)
            self.PARAMETERS_2()

    def ARGUMENTS_OPC(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type in [
            TipoToken.NEGATION,
            TipoToken.LESS,
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
            TipoToken.GREAT,
        ]:
            self.ARGUMENTS()

    def ARGUMENTS(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type in [
            TipoToken.NEGATION,
            TipoToken.LESS,
            TipoToken.GREAT,
            TipoToken.TRUE,
            TipoToken.FALSE,
            TipoToken.NULL,
            TipoToken.THIS,
            TipoToken.NUMBER,
            TipoToken.STRING,
            TipoToken.ID,
            TipoToken.PARENT_OPEN,
            TipoToken.SUPER,
        ]:
            self.EXPRESSION()
            self.ARGUMENTS_2()
        else:
            self.errors = True
            msg = f"No se esperaba el token: {self.preanalysis.type}"
            Interprete.error(self.preanalysis.line, msg)

    def ARGUMENTS_2(self):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == TipoToken.COMMA:
            self.matchToken(TipoToken.COMMA)
            self.EXPRESSION()
            self.ARGUMENTS_2()

    def matchToken(self, t):
        from interprete import Interprete

        if self.errors:
            return
        if self.preanalysis.type == t:
            self.i += 1
            self.preanalysis = self.tokens[self.i]
        else:
            self.errors = True
            msg = f"Se esperaba el token: {t}"
            Interprete.error(self.preanalysis.line, msg)
