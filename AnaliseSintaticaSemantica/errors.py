from sre_parse import State


def error(aut, state):
    if aut == 1:
        print("\n    -Erro sintático na declaração da biblioteca.")
    elif aut == 2:
        print("\n    -Erro sintático na estrutura básica de uma função.")
    elif aut == 2:
        print("\n    -Erro na declaração ou associação de valores a alguma variável.")
