from errors import error
from automato import AutomatonDeclarationFunction, AutomatonDeclarationVariable, AutomatonLib

lib = 1
var = 2
func = 3

# Grupo de palavras e expressões regulares
operadores = ["+", "-", "*", "/"]
reservadas = ["const", "while", "if", "#include",
              "<stdio.h>", "int", "return"]
comandoComparacao = ["==", ">=", "<=", "!=", ">", "<"]
comandoAtribuicao = ["="]
delimitadores = ["{", "}", "[", "]", "(", ")", "()", ";"]

tipos = ["int", "float"]


class Analysis:
    def __init__(self, arq, linhas):
        self.arq = arq
        self.linhas = linhas
        self.currentLine = 0
        self.state = 0
        self.maxLineFunc = 0

        self.a = AutomatonLib()
        self.b = AutomatonDeclarationFunction()
        self.c = AutomatonDeclarationVariable()

        self.validatorFunc = True
        self.validatorFinal = True

        self.validatorLib = True
        self.validatorVar = True

    def increment(self, x):
        return x+1

    def printLine(self, token, l, aut):
        print("   +----------------------------------------------+")
        print("    -Erro encontrado na linha ",
              token[0], " -> ", token[1], end=" ")
        l = self.increment(l)
        token = self.linhas[l].split()
        while token[0] == self.currentLine:
            print(token[1], end=" ")
            l = self.increment(l)
            token = self.linhas[l].split()
        error(aut, self.a.currentState)
        print("\n   +----------------------------------------------+\n")

    def loadArq(self):
        l = 0
        while l < len(self.linhas)-1:
            token = self.linhas[l].split()
            if self.currentLine != token[0]:
                self.currentLine = token[0]
            l = self.analise(token, l)
            if l == None:
                return
            # print("Currentline ", self.currentLine, " ", token[1])
            l = l + 1

    def analiseLib(self, token, l):
        while l < 2:
            token = self.linhas[l].split()
            if self.currentLine != token[0]:
                self.currentLine = token[0]
            print("COLOCANDO TOKEN : ", token[1])
            if self.a.accepts(token[1]) == False:
                self.printLine(token, l, lib)
                return
            l = l + 1
        return l

    def compareToken(self, token, l, type, aut):
        if token[2] == "Variavel/Funcao":
            if aut.accepts(token[1], isRe=True, isVariable=True) == False:
                # print("variavel :", token[1])
                self.printLine(token, l, type)
                return False
        elif token[2] == "Numero" or token[2] == "Operador":
            if aut.accepts(token[1], isRe=True) == False:
                self.printLine(token, l, type)
                return False
        else:
            if aut.accepts(token[1]) == False:
                self.printLine(token, l, type)
                return False
        return True

    def analiseFunction(self, token, l):
        returnLine = 0
        while l < len(self.linhas)-1:
            token = self.linhas[l].split()
            # print("COLOCANDO TOKEN Function : ", token[1])
            if self.b.a.lastAccept != 11:

                if token[1] != "return":
                    self.maxLineFunc = l-2
                if token[1] == "{":
                    returnLine = l+2

                if self.compareToken(token=token, l=l, type=func, aut=self.b) == False:
                    return
            elif token[1] != "return":
                if self.b.accepts(token[1], isQualquerCoisa=True) == False:
                    self.printLine(token, l, func)
                    return

            # print("Currentline ", self.currentLine, " ", token[1])
            l = l + 1
        return returnLine

    def analiseVariable(self, token, l):
        while l < self.maxLineFunc:
            token = self.linhas[l].split()
            if self.currentLine != token[0]:
                if self.c.a.accept_states[self.c.currentState] == False:
                    self.printLine(token, l, type)
                    return
                self.currentLine = token[0]
                self.c.currentState = 0
            #print("COLOCANDO TOKEN VAR : ", token[1])
            if self.compareToken(token=token, l=l, type=var, aut=self.c) == False:
                return
            # print("Currentline ", self.currentLine, " ", token[1])
            l = l + 1
        return l

    def analise(self, token, l):
        # print("TOKEN : ", token[1], " Classe : ", token[2])
        if self.state == 0:
            l = self.analiseLib(token, l)
            self.state = self.state + 1
            return l-1
        elif self.state == 1:
            l = self.analiseFunction(token, l)
            self.state = self.state + 1
            print("Linha : ", l)
            return l-2
        else:
            l = self.analiseVariable(token, l)
            self.state = self.state + 1
            return l
        # elif self.state == 1:
        #     l = self.analiseFunction(token, l)
        # else:
        #     l = self.analiseVariable(token, l)

    # def analise(self, token,  l, automatonLib, automatonFunc, automatonVar, automatoFinal):
    #     #print("TOKEN : ", token[1], " Classe : ", token[2])
    #     if token[2] == "Variavel/Funcao":

    #         if self.validatorLib == True:
    #             self.validatorLib = False
    #         if self.validatorFunc == True and automatonFunc.accepts(token[1], isRe=True, isVariable=True) == False:
    #             self.validatorFunc = False
    #         if self.validatorFinal == True and automatoFinal.accepts(token[1], isRe=True, isVariable=True) == False:
    #             self.validatorFinal = False
    #         if self.validatorVar == True and automatonVar.accepts(token[1], isRe=True, isVariable=True) == False:
    #             self.validatorVar = False
    #     elif token[2] == "Numero" or token[2] == "Operador":
    #         #print("TOKEN : ", token[1])

    #         if self.validatorLib == True:
    #             self.validatorLib = False
    #         if self.validatorFunc == True and automatonFunc.accepts(token[1], isRe=True) == False:
    #             self.validatorFunc = False
    #         if self.validatorFinal == True and automatoFinal.accepts(token[1], isRe=True) == False:
    #             self.validatorFinal = False
    #         if self.validatorVar == True and automatonVar.accepts(token[1], isRe=True) == False:
    #             self.validatorVar = False
    #     else:

    #         if self.validatorLib == True and automatonLib.accepts(token[1]) == False:
    #             self.validatorLib = False
    #         if self.validatorFunc == True and automatonFunc.accepts(token[1]) == False:
    #             self.validatorFunc = False
    #         if self.validatorFinal == True and automatoFinal.accepts(token[1]) == False:
    #             self.validatorFinal = False
    #         if self.validatorVar == True and automatonVar.accepts(token[1]) == False:

    #             self.validatorVar = False
    #     # print(token)
    #     # print(l+1, " ", self.validatorLib,
    #     #       self.validatorVar, " | ", self.validatorFunc, "|", self.validatorFinal)
    #     if self.validatorLib or self.validatorVar or self.validatorFunc or self.validatorFinal:
    #         return None
    #     return False
