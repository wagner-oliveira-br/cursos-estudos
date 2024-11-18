import sqlite3

def criar_banco():
    conn = sqlite3.connect("alunos.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            matricula INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            curso TEXT NOT NULL,
            data_nascimento TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

criar_banco()

import sqlite3

def cadastrar_aluno(nome, matricula, curso, data_nascimento):
    conn = sqlite3.connect("alunos.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO alunos (matricula, nome, curso, data_nascimento)
        VALUES (?, ?, ?, ?)
    """, (matricula, nome, curso, data_nascimento))

    conn.commit()
    conn.close()

def consultar_aluno(nome=None, matricula=None):
    conn = sqlite3.connect("alunos.db")
    cursor = conn.cursor()

    if nome:
        cursor.execute("SELECT * FROM alunos WHERE nome LIKE ?", ('%' + nome + '%',))
    elif matricula:
        cursor.execute("SELECT * FROM alunos WHERE matricula = ?", (matricula,))
    else:
        return []

    alunos = cursor.fetchall()
    conn.close()
    return alunos

def excluir_aluno(matricula):
    conn = sqlite3.connect("alunos.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM alunos WHERE matricula = ?", (matricula,))

    conn.commit()
    conn.close()

def pesquisar_por_curso(curso):
    conn = sqlite3.connect("alunos.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alunos WHERE curso LIKE ?", ('%' + curso + '%',))

    alunos = cursor.fetchall()
    conn.close()
    return alunos

def gerar_relatorio(ordenar_por="nome"):
    conn = sqlite3.connect("alunos.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM alunos ORDER BY {ordenar_por}")

    alunos = cursor.fetchall()
    conn.close()
    return alunos

import tkinter as tk
from tkinter import messagebox, simpledialog

def atualizar_listagem():
    listbox.delete(0, tk.END)
    alunos = gerar_relatorio()
    for aluno in alunos:
        listbox.insert(tk.END, f"Matricula: {aluno[0]}, Nome: {aluno[1]}, Curso: {aluno[2]}, Nascimento: {aluno[3]}")

def cadastrar():
    nome = simpledialog.askstring("Nome", "Digite o nome do aluno:")
    matricula = simpledialog.askinteger("Matrícula", "Digite a matrícula do aluno:")
    curso = simpledialog.askstring("Curso", "Digite o curso do aluno:")
    data_nascimento = simpledialog.askstring("Data de Nascimento", "Digite a data de nascimento do aluno (dd/mm/yyyy):")

    if nome and matricula and curso and data_nascimento:
        cadastrar_aluno(nome, matricula, curso, data_nascimento)
        atualizar_listagem()
        messagebox.showinfo("Cadastro", "Aluno cadastrado com sucesso!")
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

def consultar():
    nome = simpledialog.askstring("Nome", "Digite o nome do aluno para consulta:")
    matricula = simpledialog.askinteger("Matrícula", "Digite a matrícula do aluno para consulta:")

    if nome:
        alunos = consultar_aluno(nome=nome)
    elif matricula:
        alunos = consultar_aluno(matricula=matricula)
    else:
        messagebox.showerror("Erro", "Digite um nome ou matrícula.")
        return

    if alunos:
        for aluno in alunos:
            messagebox.showinfo("Resultado", f"Matricula: {aluno[0]}\nNome: {aluno[1]}\nCurso: {aluno[2]}\nNascimento: {aluno[3]}")
    else:
        messagebox.showinfo("Resultado", "Aluno não encontrado.")

def excluir():
    matricula = simpledialog.askinteger("Matrícula", "Digite a matrícula do aluno a ser excluído:")

    if matricula:
        excluir_aluno(matricula)
        atualizar_listagem()
        messagebox.showinfo("Exclusão", "Aluno excluído com sucesso!")

def pesquisar_por_curso_func():
    curso = simpledialog.askstring("Curso", "Digite o nome do curso para pesquisa:")
    if curso:
        alunos = pesquisar_por_curso(curso)
        listbox.delete(0, tk.END)
        if alunos:
            for aluno in alunos:
                listbox.insert(tk.END, f"Matricula: {aluno[0]}, Nome: {aluno[1]}, Curso: {aluno[2]}, Nascimento: {aluno[3]}")
        else:
            listbox.insert(tk.END, "Nenhum aluno encontrado.")

def gerar_relatorio_func():
    alunos = gerar_relatorio()
    listbox.delete(0, tk.END)
    if alunos:
        for aluno in alunos:
            listbox.insert(tk.END, f"Matricula: {aluno[0]}, Nome: {aluno[1]}, Curso: {aluno[2]}, Nascimento: {aluno[3]}")
    else:
        listbox.insert(tk.END, "Nenhum aluno encontrado.")

def sair():
    root.quit()

root = tk.Tk()
root.title("Sistema de Cadastro de Alunos")

menu = tk.Menu(root)
root.config(menu=menu)

menu_cadastro = tk.Menu(menu)
menu.add_cascade(label="Cadastro", menu=menu_cadastro)
menu_cadastro.add_command(label="Cadastrar Aluno", command=cadastrar)
menu_cadastro.add_command(label="Consultar Aluno", command=consultar)
menu_cadastro.add_command(label="Excluir Aluno", command=excluir)

menu_pesquisa = tk.Menu(menu)
menu.add_cascade(label="Pesquisa", menu=menu_pesquisa)
menu_pesquisa.add_command(label="Pesquisar por Curso", command=pesquisar_por_curso_func)

menu_relatorio = tk.Menu(menu)
menu.add_cascade(label="Relatório", menu=menu_relatorio)
menu_relatorio.add_command(label="Gerar Relatório", command=gerar_relatorio_func)

menu.add_command(label="Sair", command=sair)

listbox = tk.Listbox(root, width=80, height=20)
listbox.pack(pady=10)

atualizar_listagem()

root.mainloop()
