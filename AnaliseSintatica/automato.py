from ast import operator
import re

inteiros = "[0-9]*"
floats = "[\d*].[\d*]"
doubles = "[\d*].[\d*]"
chars = "[\"^(0-9)\"]"
operators = "[+*/-]"

names = "\D[a-zA-z0-9]*"


def increment(x):
    return x+1


class Automaton:
    def __init__(self, nstates):
        self.transitions = [{} for i in range(nstates)]
        self.accept_states = [False] * nstates

    def register(self, source_state, token, target_state):
        self.transitions[source_state][token] = target_state

    def register_accept(self, state):
        self.accept_states[state] = True

    def accept(self, state, token):
        try:
            state = self.transitions[state][token]
            return state
        except KeyError:
            return False


class AutomatonLib:
    def __init__(self):
        self.a = Automaton(3)
        self.registers()
        self.currentState = 0

    def registers(self):
        self.a.register(0, '#include', 1)
        self.a.register(1, "<stdio.h>", 2)
        self.a.register_accept(2)

    def accepts(self, token):
        result = self.a.accept(self.currentState, token)
        if result == False:
            return False
        self.currentState = result
        return True


class AutomatonDeclaration():
    def __init__(self, nStates):
        self.a = Automaton(nStates)
        self.registers()
        self.currentState = 0

    def registers(self):
        # Interação 2
        self.a.register(1, names, 4)
        self.a.register(2, names, 5)
        self.a.register(3, names, 6)

        # Interação 3
        self.a.register(4, "=", 7)
        self.a.register(5, "=", 8)
        self.a.register(6, "=", 9)

        # Interação 4
        self.a.register(7, inteiros, 10)
        self.a.register(8, floats, 11)
        self.a.register(9, chars, 12)

        self.a.register(10, ";", 13)
        self.a.register(11, ";", 13)
        self.a.register(12, ";", 13)

    def analysisRe(self, token):
        result = False
        # if (re.match(chars, token)) != None:
        #     print("token : ", token)
        #     result = self.a.accept(self.currentState, chars)
        #     return result
        if (re.match(operators, token)) != None and result == False:
            result = self.a.accept(self.currentState, operators)
        if (re.match(floats, token)) != None and result == False:
            result = self.a.accept(self.currentState, floats)
        if (re.match(doubles, token)) != None and result == False:
            result = self.a.accept(self.currentState, doubles)
        if (re.match(inteiros, token)) != None and result == False:
            result = self.a.accept(self.currentState, inteiros)

        return result

    def accepts(self, token, isRe=False, isVariable=False, isQualquerCoisa=False):
        result = False
        if isQualquerCoisa:
            result = self.currentState
        elif isRe and isVariable:
            if (re.match(names, token)) != None:
                result = self.a.accept(self.currentState, names)
        elif isRe:
            result = self.analysisRe(token)

        else:
            result = self.a.accept(self.currentState, token)

        if result == False or result == None:
            return False
        self.currentState = result
        return True


class AutomatonDeclarationVariable(AutomatonDeclaration):
    def __init__(self):
        super().__init__(18)
        # Interação 1
        self.a.register(0, 'int', 1)
        self.a.register(0, "float", 2)
        self.a.register(0, "double", 2)
        self.a.register(0, "char", 3)

        self.a.register(4, ";", 11)
        self.a.register(5, ";", 11)
        self.a.register(6, ";", 11)

        # Interação 3
        self.a.register(10, operators, 14)
        self.a.register(14, names, 16)
        self.a.register(14, inteiros, 16)
        self.a.register(16, operators, 14)

        self.a.register(11, operators, 15)
        self.a.register(15, names, 17)
        self.a.register(15, floats, 17)

        self.a.register(17, operators, 115)

        self.a.register(16, ";", 13)
        self.a.register(17, ";", 13)

        # Interação 5
        self.a.register(10, ";", 11)

        self.a.register_accept(11)


class AutomatonDeclarationFunction(AutomatonDeclaration):
    def __init__(self):
        super().__init__(23)
        # interação 1
        self.a.register(0, "int", 17)
        self.a.register(0, "float", 18)
        self.a.register(0, "double", 18)
        self.a.register(0, "char", 19)
        self.a.register(0, "void", 20)

        # interação 2
        self.a.register(17, names, 21)
        self.a.register(18, names, 21)
        self.a.register(19, names, 21)
        self.a.register(20, names, 21)

        # interação 3
        self.a.register(21, "(", 22)
        self.a.register(21, "()", 11)

        # interação 4
        self.a.register(22, 'int', 1)
        self.a.register(22, "float", 2)
        self.a.register(22, "double", 2)
        self.a.register(22, "char", 3)

        self.a.register(22, "void", 10)
        self.a.register(1, names, 10)
        self.a.register(2, names, 10)
        self.a.register(3, names, 10)

        # interação 8
        self.a.register(10, ")", 11)
        self.a.register(10, ",", 0)
        # interação 9
        self.a.register(11, "{", 12)
        # interação 10
        self.a.register(12, "\w", 12)
        self.a.register(12, "return", 13)
        # interação 11
        self.a.register(13, inteiros, 14)
        # interação 12
        self.a.register(14, ";", 15)
        # incteração 13
        self.a.register(15, "}", 16)


# a = AutomatonDeclarationVariable()
# print(a.accepts("int"))
# print(a.accepts("azul4", isRe=True, isVariable=True))
# print(a.accepts("="))

# print(a.accepts("20", isRe=True))
# print(a.accepts("+", isRe=True))
# print(a.accepts("20", isRe=True))
# print(a.accepts(";"))


# a = AutomatonDeclarationFunction()
# print(a.accepts("int"))
# print(a.accepts("main", isRe=True, isVariable=True))
# print(a.accepts("("))
# print(a.accepts("void"))
# print(a.accepts(")"))
# print(a.accepts("{"))
# print(a.accepts("qualquerCoisa", isQualquerCoisa=True))
# print(a.accepts("return"))
# print(a.accepts("1", isRe=True))
# print(a.accepts(";"))
# print(a.accepts("}"))


# a = AutomatonLib()
# print(a.accepts("#include"))
# print(a.accepts("<stdio.h>"))
