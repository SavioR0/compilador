import re

from automato import AutomatonLib

# Grupo de palavras e expressões regulares
operadores = ["+", "-", "*", "/"]
reservadas = ["const", "while", "if", "#include",
              "<stdio.h>", "int", ";", "return"]
comandoComparacao = ["==", ">=", "<=", "!=", ">", "<"]
comandoAtribuicao = ["="]
delimitadores = ["{", "}", "[", "]", "(", ")", "()"]

tipos = ["int", "float"]


class Analysis:
    def __init__(self, arq, linhas):
        self.arq = arq
        self.linhas = linhas
        self.currentLine = 0
        self.automatonLib = AutomatonLib()

        self.validatorFunc = True
        self.validatorLib = True
        self.validatorVar = True

    def reloadValidators(self):
        self.validatorFunc = True
        self.validatorLib = True
        self.validatorVar = True

    def increment(self, x):
        return x+1

    def printLine(self, token, l):
        print("Erro encontrado na linha ",
              self.currentLine, " -> ", token[1], end=" ")
        l = self.increment(l)
        token = self.linhas[l].split()
        while token[0] == self.currentLine:
            print(token[1], end=" ")
            l = self.increment(l)
            token = self.linhas[l].split()

    def analise(self, token,  l, automatonLib, automatonFunc, automatonVar):
        if token[2] == "Reservado" or token[2] == "Atribuicao":

            if self.validatorLib == True and automatonLib.accepts(token[1]) == False:
                self.validatorLib = False
            if self.validatorFunc == True and automatonFunc.accepts(token[1]) == False:
                self.validatorFunc = False
            if self.validatorVar == True and automatonVar.accepts(token[1]) == False:
                self.validatorVar = False
        elif token[2] == "Variavel/Funcao":
            print("TOKEN :", token[2])

            if self.validatorLib == True:
                self.validatorLib = False
            if self.validatorFunc == True and automatonFunc.accepts(token[1], isRe=True, isVariable=True) == False:
                self.validatorFunc = False
            if self.validatorVar == True and automatonVar.accepts(token[1], isRe=True, isVariable=True) == False:
                self.validatorVar = False
        #TODO: Numeros
        print(token)
        print(self.validatorLib, self.validatorFunc, self.validatorVar)
        return None

    def analiseLib(self, token, l):
        return False

    def analiseType(self, currentLine, token, linhas, l):
        return False

    def analiseFunction(self, currentLine, token, linhas, l):
        return False