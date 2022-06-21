# Compilador
Trabalho prático de compiladores feito em python para a linguagem C em um cenário limitado e controlado. Nesse sentido, do tabalho foi feito:

<ul>
<li>Análise léxica</li>
<li>Análise Sintática</li>
<li>Análise Semântica</li>

</ul>

## Compilação
Toda a codificação foi feita em linguagem Python.
O arquivo principal "main.py" é responsável por chamar todas as análises (léxica, sintática e semântica).
No código :

```
lexica("../compilador/codigos/<codigo para teste>.txt")
```

Essa linha é a responsável por mudar os arquivos de teste, trocando o texto entre "<>" pelo nome do código que deseja realizar os teste. 

`
Ex: lexica("../compilador/codigos/Codigo 10.txt")
`

A execução do arquivo principal, retornará os resultados obtidos pela compilação.

## Análise léxica
 A análise léxica foi desenvolvida a partir do aquivo "codigo.txt", ou seja, um ambiente controlado. Para tanto foram implementadas na análise a leitura dos símbolos respeitando o quadro a seguir:

 <img src="arquivos\quadro.png">

## Análise Sintática e Semântica
A análise sintática foram usados três autômatos para representar as estruturas de declaração das bibliotecas, funções e expressões juntamente com a declaração de variáveis. A ilustração a seguir mostra como ficou a modelagem.
  <img src=https://github.com/SavioR0/compilador/issues/2#issue-1277717647>

Todos os testes realizados para a validação do compilador foram feitos a partir dos códigos disponibilizados na pasta "codigos", os quais apresentam alguns erros comuns na validação semântico. 

## Obstáculos
Pela disponibilidade de tempo e a grande carga horário já dedicada ao trabalho alguns pontos ficaram faltando na entrega final. Com isso, a função for por exemplo, antes presente no código 4 foi excluída.

Todos warnings que são considerados em compiladores C foram identificados como erros, portanto é feita a interrompção da compilação quando é encontrado.

Todas as variáveis não declaradas e que são usadas são identificadas e relatados os erros semânticos. 

No código de teste 6 a divisão por zero não é considerada como erro em nenhuma das análises, por ocorrer apenas um "Floating point exception".

Aspas duplas e aspas simples foram considerados como representação de vetores de caracteres.
