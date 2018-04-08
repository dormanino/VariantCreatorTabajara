from Parser.CodeRuleParser import CodeRuleParser

lista1 = ["GC2", "AM3", "AR1"]
lista2 = ["GH4", "GK9", "AM3", "N58"]
lista3 = ["GH8", "AM4", "AP6"]
lista4 = ["GC2", "G02", "AM3", "AQ3"]
lista5 = ["GE3", "GH4", "AX6", "GK8"]
lista6 = ["N57", "GE2", "M58", "GK8"]

# condicao = "((GC2/GH4+-GK8/GH8+-AX6)+(AM3/AM4)+(AP1/AP3/AP6/AP9/AQ3/AQ7/AR1))"
# condicao = "((GC2/GH4+-GK8/GH8+-AX6)+(AM3/AM4)+(AP1/AP3/AP6/AP9/AQ3/AQ7/AR1)/GC2+G02+AM3+(AP6/AP9/AQ3/AQ7/AR1));"
# condicao = "+-((N56/N57)+(GE2/GE3/GE7))+M58/GH4+GK8/GH8+AX6;"
condicao = "((GC2/GH4+-GK8/GH8+-AX6)+(AM3/AM4)+(AP1/AP3/AP6/AP9/AQ3/AQ7/AR1)/GC2+G02+AM3+(AP6/AP9/AQ3/AQ7/AR1))/+-((N56/N57)+(GE2/GE3/GE7))+M58/GH4+GK8/GH8+AX6;"

listas = [lista1, lista2, lista3, lista4, lista5, lista6]

for index, lista in enumerate(listas):
    resultado = CodeRuleParser.validate(condicao, lista);
    valido = 'Verdadeiro' if resultado else "Falso"
    print("LISTA " + str(index+1) + ": " + valido)