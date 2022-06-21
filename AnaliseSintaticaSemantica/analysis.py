from AnaliseSintaticaSemantica.automato import AutomatonDeclarationFunction, AutomatonDeclarationVariable, AutomatonLib
from AnaliseSintaticaSemantica.errors import error

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

    def printLine(self, token, l, type, lastState, palavra):
        print("+---------------------ERROR---------------------------+")
        print(" -Erro encontrado na linha ",
              token[0], " -> ", token[1], end=" ")
        l = self.increment(l)
        token = self.linhas[l].split()
        while token[0] == self.currentLine:
            print(token[1], end=" ")
            l = self.increment(l)
            token = self.linhas[l].split()
        error(type, lastState, palavra)
        print("+----------------------------------------------------+")

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
        return True

    def analiseLib(self, token, l):
        while l < 2:
            token = self.linhas[l].split()
            if self.currentLine != token[0]:
                self.currentLine = token[0]
            #print("COLOCANDO TOKEN : ", token[1])
            if self.a.accepts(token[1]) == False:
                self.printLine(token, l, "Sintático",
                               self.a.a.lastAccept[0], token[1])
                return
            l = l + 1
        return l

    def compareToken(self, token, l, type, aut):
        if token[2] == "Variavel/Funcao":
            if token[1] in self.b.variables and aut == self.c and aut.currentState == 0:
                self.c.currentState = 1
                #print("CURRENT : ", self.c.currentState)
            validator = aut.accepts(token[1], isRe=True, isVariable=True)
            if (validator == False) or ((validator == True) and (aut == self.c) and ((self.c.currentState != 4 and self.c.currentState != 5 and self.c.currentState != 6) and (token[1] not in self.b.variables))):
                # print("variavel :", token[1],
                #      " State : ", self.c.a.lastAccept[0], " ", self.a.currentState)
                # print(self.b.variables)
                if validator == False:
                    if self.c.a.lastAccept != None:
                        self.printLine(token, l, "Sintático",
                                       self.c.a.lastAccept[0], token[1])
                    else:
                        self.printLine(token, l, "Sintático",
                                       None, token[1])
                else:
                    if self.c.a.lastAccept != None:
                        self.printLine(token, l, "Semântico",
                                       self.c.a.lastAccept[0], token[1])
                    else:
                        self.printLine(token, l, "Semântico",
                                       None, token[1])

                return False
            # print("variavel :", token[1], " Ultimo : ", self.c.a.lastAccept[0])
            if (aut == self.c) and (self.c.currentState == 4 or self.c.currentState == 5 or self.c.currentState == 6) and token[1] not in self.b.variables:
                # print("Adicionando variavel : ",
                #      token[1], " State : ", self.c.a.lastAccept[0])
                self.b.variables.append(token[1])
        elif token[2] == "Numero" or token[2] == "Operador":
            if aut.accepts(token[1], isRe=True) == False:
                self.printLine(token, l, "Sintático",
                               aut.a.lastAccept[0], token[1])
                return False
        else:
            if aut.accepts(token[1]) == False:
                self.printLine(token, l, "Semântico",
                               aut.a.lastAccept[0], token[1])
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
                    self.printLine(token, l, "Sintático",
                                   self.b.a.lastAccept[0], token[1])
                    return

            # print("Currentline ", self.currentLine, " ", token[1])
            l = l + 1
        return returnLine

    def analiseVariable(self, token, l):
        while l < self.maxLineFunc:
            token = self.linhas[l].split()
            if self.currentLine != token[0]:
                if self.c.a.accept_states[self.c.currentState] == False:
                    self.printLine(token, l, "Sintático",
                                   self.c.a.lastAccept[0], token[1])
                    return
                self.currentLine = token[0]
                self.c.currentState = 0
            # print("COLOCANDO TOKEN VAR : ", token[1])
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
            if l == None:
                return
            return l-1
        elif self.state == 1:
            l = self.analiseFunction(token, l)
            self.state = self.state + 1
            if l == None:
                return
            return l-2
        else:
            l = self.analiseVariable(token, l)
            self.state = self.state + 1
            if l == None:
                return
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
