from analysis import Analysis


def main():
    print("\n\n\n\n")
    arq = open("tokenizacao.txt", "r")
    analise = Analysis(arq, arq.readlines())

    #print("Arquivo tem %d linhas " % len(analise.linhas))
    analise.loadArq()

    # print("\n+------ ANÁLISE LÉXICA FINALIZADA ---------+")
    # print("+------------------------------------------+\n")


main()
