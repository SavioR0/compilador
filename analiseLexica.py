import re

arq = open("codigo.txt", "r")


# Grupo de palavras e expressões regulares
operadores = ["+", "-", "*", "/"]
reservadas = ["const", "while", "if", "#include",
              "<stdio.h>", "int", ";", "return"]
comandoComparacao = ["==", ">=", "<=", "!=", ">", "<"]
comandoAtribuicao = ["="]
delimitadores = ["{", "}", "[", "]", "(", ")"]
numeros = re.compile(r"\d")

# Tokenização
tokens = []

for x in arq:
    x = x.strip()
    lista = x.split()

    i = 0
    tam = len(lista)

    comecoString = -1

    while i < tam:
        lista[i] = lista[i].strip()
        if ";" in lista[i]:
            y = lista[i].split(";")
            tokens.append(y[0])
            tokens.append(";")
        elif ("{" or "}" or "[" or "]" or "(" or ")") in lista[i]:
            if ("(" or ")") in lista[i]:
                if "(" in lista[i]:
                    y = lista[i] .split("(")
                    tokens.append(y[0])
                    tokens.append("(")
                    y = y[1].split(")")

                    if y[1] != '':
                        tokens.append(")")
                        tokens.append(y[1])

                elif ")" in lista[i]:
                    y = lista[i] .split(")")
                    tokens.append(y[0])
                    tokens.append(")")
            elif ("{" or "}") in lista[i]:
                if "{" in lista[i]:
                    y = lista[i] .split("{")
                    tokens.append(y[0])
                    tokens.append("{")
                elif "}" in lista[i]:
                    y = lista[i] .split("}")
                    tokens.append(y[0])
                    tokens.append("}")
            elif ("[" or "]") in lista[i]:
                if "[" in lista[i]:
                    y = lista[i] .split("[")
                    tokens.append(y[0])
                    tokens.append("[")
                elif "]" in lista[i]:
                    y = lista[i] .split("]")
                    tokens.append(y[0])
                    tokens.append("]")
        elif "\"" in lista[i]:
            if comecoString == -1:
                comecoString = i
            else:
                tokenLiteral = ""
                for j in range((i - comecoString)+1):
                    tokenLiteral = tokenLiteral + lista[j + comecoString] + " "
                tokens.append(tokenLiteral)
                comecoString = -1

        else:
            tokens.append(lista[i])

        i = i + 1
arq.close


# Classificando os tokens
arq = open("tokenizacao.txt", "w")
for x in tokens:
    if x in reservadas:
        arq.write(x + " Reservado\n")
    elif x in operadores:
        arq.write(x + " Operador\n")
    elif x in comandoComparacao:
        arq.write(x + " Comparacao\n")
    elif x in comandoAtribuicao:
        arq.write(x + " Atribuicao\n")
    elif x in delimitadores:
        arq.write(x + " Delimitador\n")
    elif "\"" in x:
        arq.write(x + " Literal\n")
    elif((re.match(numeros, x)) != None):
        arq.write(x + " Numero\n")
    elif x != "":
        arq.write(x + " Variavel/Funcao\n")

print("\n+------ ANÁLISE LÉXICA FINALIZADA ---------+")
print("|    Arquivo resultado: \"tokenizacao.txt\"  |")
print("+------------------------------------------+\n")
