import re

inteiros = "[0-9]*"
floats = "[\d*].[\d*]"
doubles = "[\d*].[\d*]"
chars = '""'
operators = "[+*/-]"

names = "\D[a-zA-z0-9]*"
numeros = r"[0-9][\.]?[^\,]"

# names = "^\D"


def increment(x):
    return x+1


class Automaton:
    def __init__(self, nstates):
        self.transitions = [{} for i in range(nstates)]
        self.accept_states = [False] * nstates
        self.lastAccept = None

    def register(self, source_state, token, target_state):
        self.transitions[source_state][token] = target_state

    def register_accept(self, state):
        self.accept_states[state] = True

    def accept(self, state, token):
        try:
            state = self.transitions[state][token]
            #print("STATE :", state, " Token : ", token)

            self.lastAccept = [state, token]
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
        self.currentState = 0
        self.validator = True
        self.registers()

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
        self.a.register(7, names, 10)
        self.a.register(8, floats, 11)
        self.a.register(8, inteiros, 11)
        self.a.register(8, names, 11)
        self.a.register(9, chars, 12)
        self.a.register(9, names, 12)

        self.a.register(10, ";", 13)
        self.a.register(11, ";", 13)
        self.a.register(12, ";", 13)

    def analysisRe(self, token):
        result = False
        #print("TOKEN : ", token)
        if (re.match(chars, token)) != None:
            #print("LENDO CHAR : ", token)
            result = self.a.accept(self.currentState, chars)
        #     return result
        if (re.match(operators, token)) != None and result == False:
            result = self.a.accept(self.currentState, operators)
        if (re.match(floats, token)) != None and result == False:
            result = self.a.accept(self.currentState, floats)
        if (re.match(doubles, token)) != None and result == False:
            result = self.a.accept(self.currentState, doubles)
        if (re.match(inteiros, token)) != None and result == False:
            result = self.a.accept(self.currentState, inteiros)
        # print(result)
        return result

    def accepts(self, token, isRe=False, isVariable=False, isQualquerCoisa=False):
        result = False
        # self.currentState = 0
        if self.validator == True:
            if isQualquerCoisa:
                result = self.currentState
            elif isRe and isVariable:
                if (re.match(names, token)) != None:
                    result = self.a.accept(self.currentState, names)
                    #print('STATE : ', result)
            elif isRe:
                result = self.analysisRe(token)

            else:
                result = self.a.accept(self.currentState, token)

        if result == False or result == None:
            self.validator = False
            return False
        self.currentState = result
        return True


class AutomatonDeclarationVariable(AutomatonDeclaration):
    def __init__(self, **kwargs):
        super().__init__(24)
        if kwargs.get('current') is not None:
            self.currentState = kwargs.get('current')
        else:
            self.currentState = 0
        self.accept_States = self.a.accept_states
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
        self.a.register(10, "%", 14)
        self.a.register(14, names, 16)
        self.a.register(14, inteiros, 16)
        self.a.register(16, operators, 14)
        self.a.register(16, "%", 14)

        self.a.register(11, operators, 15)
        self.a.register(15, names, 17)
        self.a.register(15, floats, 17)

        self.a.register(17, operators, 115)

        self.a.register(16, ";", 13)
        self.a.register(17, ";", 13)

        self.a.register(14, "(", 18)
        self.a.register(15, "(", 19)
        # Interação 5
        self.a.register(10, ",", 1)
        self.a.register(11, ",", 2)
        self.a.register(12, ",", 3)

        self.a.register(16, ",", 1)
        self.a.register(17, ",", 2)

        # Interação 6
        self.a.register(18, operators, 18)
        self.a.register(19, operators, 19)

        self.a.register(18, inteiros, 20)
        self.a.register(18, names, 20)
        self.a.register(19, floats, 21)
        self.a.register(19, names, 21)

        # Interação 7
        self.a.register(20, operators, 18)
        self.a.register(21, operators, 19)

        # Interação 8
        self.a.register(20, ")", 22)
        self.a.register(21, ")", 23)

        # Interação 9
        self.a.register(22, ";", 13)
        self.a.register(23, ";", 13)

        self.a.register_accept(13)


class AutomatonDeclarationFunction(AutomatonDeclaration):
    # def __init__(self, **kwargs):
    #     super().__init__(18)
    #     if kwargs.get('current_state'):
    #         self.currentState = kwargs.get('current_state')
    #     self.registers()

    def __init__(self, **kwargs):
        super().__init__(23)
        self.variables = []
        if kwargs.get('current') is not None:
            self.currentState = kwargs.get('current')
        else:
            self.currentState = 0

        # self.accept_States = self.a.accept_states

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
        self.a.register(12, names, 12)
        self.a.register(12, inteiros, 12)
        self.a.register(12, chars, 12)
        self.a.register(12, operators, 12)
        self.a.register(12, floats, 12)

        self.a.register(12, "=", 12)
        self.a.register(12, ',', 12)

        self.a.register(12, 'int', 12)
        self.a.register(12, "float", 12)
        self.a.register(12, "double", 12)
        self.a.register(12, "char", 12)

        self.a.register(12, ";", 12)
        self.a.register(12, "(", 12)
        self.a.register(12, ")", 12)

        self.a.register(12, "return", 13)
        # interação 11
        self.a.register(13, inteiros, 14)
        # interação 12
        self.a.register(14, ";", 15)
        # incteração 13
        self.a.register(15, "}", 16)

        self.a.register_accept(16)


# a = b + c - 7 * e / a * d - a + 10 / ( c + d + 10 );
# aut = AutomatonDeclarationVariable()
# print(aut.accepts("int"))
# print(aut.accepts("a",  isRe=True, isVariable=True))
# print(aut.accepts("="))
# print(aut.accepts("b",  isRe=True, isVariable=True))
# print(aut.accepts("+", isRe=True))
# print(aut.accepts("c", isRe=True))
# print(aut.accepts("-", isRe=True))
# print(aut.accepts("7", isRe=True))
# print(aut.accepts("*", isRe=True))
# print(aut.accepts("("))
# print(aut.accepts("e", isRe=True, isVariable=True))
# print(aut.accepts("/", isRe=True))
# print(aut.accepts("a", isRe=True, isVariable=True))
# print(aut.accepts(")"))
# print(aut.accepts(";"))
# print("A validação do automato é : ", aut.a.accept_states[aut.currentState])


# aut = AutomatonDeclarationVariable()
# print(aut.accepts("int"))
# print(aut.accepts("azukl", isRe=True, isVariable=True))
# print(aut.accepts("="))
# print(aut.accepts("20", isRe=True))
# print(aut.accepts("+", isRe=True))
# print(aut.accepts("20", isRe=True))
# print(aut.accepts(","))
# print(aut.accepts("azul", isRe=True, isVariable=True))
# print(aut.accepts("="))
# print(aut.accepts("25", isRe=True))
# print(aut.accepts(";"))
# print("A validação do automato é : ", aut.a.accept_states[aut.currentState])

# a = AutomatonDeclarationFunction()
# print(a.accepts("int"))
# print(a.accepts("main", isRe=True, isVariable=True))
# print(a.accepts("()"))
# print(a.accepts("{"))
# print(a.accepts("qualquerCoisa", isQualquerCoisa=True))
# print(a.accepts("return"))
# print(a.accepts("1", isRe=True))
# print(a.accepts(";"))
# print(a.accepts("}"))
# print(a.accepts(";"))
# print("A validação do automato é : ", a.a.accept_states[a.currentState])


# a = AutomatonLib()
# print(a.accepts("#include"))
# # print(a.accepts("<stdio.h>"))
# print("A validação do automato é : ", a.a.accept_states[a.currentState])
