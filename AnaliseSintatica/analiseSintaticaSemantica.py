
from automato import AutomatonLib, AutomatonDeclarationFunction, AutomatonDeclarationVariable
from analysis import Analysis


arq = open("tokenizacao.txt", "r")

analise = Analysis(arq, arq.readlines())


print("Arquivo tem %d linhas " % len(analise.linhas))
l = 0
a = AutomatonLib()
b = AutomatonDeclarationFunction()
c = AutomatonDeclarationVariable()

while l < len(analise.linhas):
    token = analise.linhas[l].split()
    if analise.currentLine != token[0]:
        a = AutomatonLib()
        b = AutomatonDeclarationFunction()
        c = AutomatonDeclarationVariable()
        analise.reloadValidators()
        analise.currentLine = token[0]
    if analise.analise(token, l, a, b, c) != None:
        analise.printLine(token, l)
        break
    #print("Currentline ", analise.currentLine, " ", token[1])

    l = l + 1


# print("\n+------ ANÁLISE LÉXICA FINALIZADA ---------+")
# print("|    Arquivo resultado: \"tokenizacao.txt\"  |")
# print("+------------------------------------------+\n")
