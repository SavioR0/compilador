from sre_parse import State


def error(aut, state):

    print("\n    -[Erro] Tipo :", aut, " ->", end="")
    if state == 16:
        print(" É esperado receber um tipo \"int\"")
