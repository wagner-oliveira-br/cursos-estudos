'''
"enumerate" função que lista em sequência numérica horizontal, as vezes usado para saber índice do objeto dentro do laço for.
'''
alunos = ["joao", "pedro", "maria", "vitor"]
for indice, alunos in enumerate(alunos):
    print(f"{indice}: {alunos}")