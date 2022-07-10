from AnaliseLexica.analiseLexica import lexica
from AnaliseSintaticaSemantica.analiseSintaticaSemantica import sintaticaSemantica
from Conversor_C_Python.conversor import conversor


def main():
    arq = "../compilador/codigos/Código 1.txt"
    lexica(arq)
    if sintaticaSemantica():
        conversor(arq)


main()
