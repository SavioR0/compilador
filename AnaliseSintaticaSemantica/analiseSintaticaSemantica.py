

from AnaliseSintaticaSemantica.analysis import Analysis


def sintaticaSemantica():
    print("\n")
    arq = open("tokenizacao.txt", "r")
    analise = Analysis(arq, arq.readlines())

    #print("Arquivo tem %d linhas " % len(analise.linhas))
    if analise.loadArq() == True:
        print("+------ ANÁLISE SINTÁTICA E SEMÂNTICA FINALIZADA --------+")
        print("+--------------------------------------------------------+\n")
