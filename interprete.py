
import sys
from scanner import Scanner
from parserr import Parser
from postfixgen import Postfix
from nodo import Nodo
from generadorAST import GeneradorAST
from tablasimbolos import init


class Interprete:
    # Clase principal del intérprete

    def __init__(self) -> None:
        self.existenErrores = False

    def ejecutarArchivo(self, archivo):
        # Método para ejecutar un archivo con código

        with open(archivo, "r") as file:
            lineas = file.readlines()

        self.ejecutar(lineas)

        if self.existenErrores:
            sys.exit()

    def ejecutarPrompt(self):
        # Método para ejecutar el prompt del intérprete

        lineas = []
        while True:
            try:
                linea = input("Compilador:")
                lineas.append(linea)
            except EOFError:
                break
            if not linea:
                continue
            self.ejecutar(lineas)
            lineas.clear()

    def error(linea, msj):
        # Método para reportar un error encontrado durante la ejecución del código
        print(f"[line {linea}] | {msj}")
        pass
        # self.report(self, msg, lin)

    def reportar(self, linea, donde, mensaje):
        # Método para reportar información al usuario durante la ejecución del código
        pass

    def ejecutar(self, source):
        # Método para ejecutar el código ingresado

        self.scanner = Scanner(source)
        self.tokens = self.scanner.ScanTokens()
        self.parser = Parser(self.tokens)
        self.parser.parse()
        self.postfix = Postfix(self.tokens)
        self.postfija = self.postfix.convertir()
        self.genAst = GeneradorAST(self.postfija)
        self.programa = self.genAst.generarAST()
        self.programa.recorrer()


def main():
    # Función principal del intérprete
    interprete = Interprete()
    init()

    if len(sys.argv) > 2:
        print("Uso: interprete [script]")
        sys.exit()
    if len(sys.argv) == 2:
        interprete.ejecutarArchivo(sys.argv[1])
    else:
        interprete.ejecutarPrompt()


if __name__ == "__main__":
    main()
