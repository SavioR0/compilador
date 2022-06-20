from sre_parse import State


def error(aut, state, token):

    print("\n    -[Erro] Tipo :", aut, " ->", end="")
    if state == 10:
        print(" Operador inválido para esse tipo")
    if state == 16:
        print(" É esperado receber um tipo \"int\", variavel",
              token, " não pode ser aceita")
    if state == 12:
        print(" Tipo recebido inválido")
    if state == 13:
        print(" Variavel ",token,"não foi declarada anteriormente")
