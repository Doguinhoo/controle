import tkinter as tk
import deps

# tipo: "voluntário" ou "abrigado"


def entrada(tipo):
    janela = tk.Tk()
    janela.resizable(False, False)
    janela.tk.call('tk', 'scaling', 8.0)
    janela.title(f"Entrada de {tipo}")

    teste = tk.Frame(master=janela)
    etiquetas = tk.Frame(master=teste)
    entradas = tk.Frame(master=teste)

    tk.Label(master=etiquetas, text="Nome:").pack()
    nome = tk.Entry(master=entradas)
    nome.pack()

    tk.Label(master=etiquetas, text="CPF:").pack()
    cpf = tk.Entry(master=entradas, text="XXX.XXX.XXX-XX")
    cpf.pack()

    tk.Label(master=etiquetas, text="RG:").pack()
    rg = tk.Entry(master=entradas)
    rg.pack()

    tk.Label(master=etiquetas, text="Profissão:").pack()
    profissao = tk.Entry(master=entradas)
    profissao.pack()

    tk.Label(master=etiquetas, text="Área de atuação:").pack()
    area = tk.Entry(master=entradas)
    area.pack()

    tk.Label(master=etiquetas, text="Telefone:").pack()
    telefone = tk.Entry(master=entradas)
    telefone.pack()

    etiquetas.pack(side=tk.LEFT)
    entradas.pack(side=tk.LEFT)
    teste.pack()

    tk.Button(text="Enviar", command=enviarEntrada).pack()

    janela.mainloop()


def enviarEntrada():
    pass


def main():
    entrada("voluntário")


if __name__ == "__main__":
    main()
