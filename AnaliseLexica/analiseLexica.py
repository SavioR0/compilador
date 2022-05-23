from operator import index
import re

arq = open("codigo.txt", "r")


# Grupo de palavras e expressões regulares
operadores = ["+", "-", "*", "/"]
reservadas = ["const", "while", "if", "#include",
              "<stdio.h>", "int", "return"]
comandoComparacao = ["==", ">=", "<=", "!=", ">", "<"]
comandoAtribuicao = ["="]
delimitadores = ["{", "}", "[", "]", "(", ")", "()", ";"]
numeros = re.compile(r"\d")

# Tokenização
tokens = []
linha = 0

for x in arq:
    linha = linha + 1
    x = x.strip()
    lista = x.split()

    i = 0
    tam = len(lista)

    comecoString = -1

    while i < tam:

        lista[i] = lista[i].strip()
        if ";" in lista[i]:
            y = lista[i].split(";")
            tokens.append(str(linha) + " " + y[0])
            tokens.append(str(linha) + " " + ";")
        elif ("{" or "}" or "[" or "]" or "(" or ")") in lista[i]:
            if ("(" or ")") in lista[i]:
                if "(" in lista[i]:
                    y = lista[i] .split("(")
                    tokens.append(str(linha) + " " + y[0])
                    tokens.append(str(linha) + " " + "(")
                    y = y[1].split(")")

                    if y[1] != '':
                        tokens.append(str(linha) + " " + ")")
                        tokens.append(str(linha) + " " + y[1])

                elif ")" in lista[i]:
                    y = lista[i] .split(")")
                    tokens.append(str(linha) + " " + y[0])
                    tokens.append(str(linha) + " " + ")")
            elif ("{" or "}") in lista[i]:
                if "{" in lista[i]:
                    y = lista[i] .split("{")
                    tokens.append(str(linha) + " " + y[0])
                    tokens.append(str(linha) + " " + "{")
                elif "}" in lista[i]:
                    y = lista[i] .split("}")
                    tokens.append(str(linha) + " " + y[0])
                    tokens.append(str(linha) + " " + "}")
            elif ("[" or "]") in lista[i]:
                if "[" in lista[i]:
                    y = lista[i] .split("[")
                    tokens.append(str(linha) + " " + y[0])
                    tokens.append(str(linha) + " " + "[")
                elif "]" in lista[i]:
                    y = lista[i] .split("]")
                    tokens.append(str(linha) + " " + y[0])
                    tokens.append(str(linha) + " " + "]")
        elif "\"" in lista[i]:
            if comecoString == -1:
                comecoString = i
            else:
                tokenLiteral = str(linha) + " "
                for j in range((i - comecoString)+1):
                    tokenLiteral = tokenLiteral + lista[j + comecoString] + " "
                tokens.append(tokenLiteral)
                comecoString = -1

        else:
            tokens.append(str(linha) + " " + lista[i])

        i = i + 1
arq.close


# Classificando os tokens
arq = open("tokenizacao.txt", "w")
for x in tokens:
    aux = x[2:]
    if aux in reservadas:
        arq.write(x + " Reservado\n")
    elif aux in operadores:
        arq.write(x + " Operador\n")
    elif aux in comandoComparacao:
        arq.write(x + " Comparacao\n")
    elif aux in comandoAtribuicao:
        arq.write(x + " Atribuicao\n")
    elif aux in delimitadores:
        arq.write(x + " Delimitador\n")
    elif "\"" in x:
        arq.write(x + " Literal\n")
    elif((re.match(numeros, aux)) != None):
        arq.write(x + " Numero\n")
    elif aux != "":
        arq.write(x + " Variavel/Funcao\n")

print("\n+------ ANÁLISE LÉXICA FINALIZADA ---------+")
print("|    Arquivo resultado: \"tokenizacao.txt\"  |")
print("+------------------------------------------+\n")