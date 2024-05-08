import tkinter as tk
from tkinter import font
import deps

# tipo: "voluntário" ou "abrigado"


def entrada(tipo):
    match tipo:
        case 'voluntário': caminho = deps.PATH_VOL
        case 'abrigado': caminho = deps.PATH_ABR

    janela = tk.Tk()
    janela.resizable(False, False)
    janela.title(f"Entrada de {tipo}")

    fonte = font.Font(size=14)
    agl = tk.Frame(master=janela)
    etiquetas = tk.Frame(master=agl)
    entradas = tk.Frame(master=agl)

    tk.Label(master=etiquetas, text="Nome:", font=fonte).pack()
    nome = tk.Entry(master=entradas, font=fonte)
    nome.pack()

    tk.Label(master=etiquetas, text="CPF:", font=fonte).pack()
    cpf = tk.Entry(master=entradas, font=fonte)
    cpf.pack()

    tk.Label(master=etiquetas, text="Profissão:", font=fonte).pack()
    profissao = tk.Entry(master=entradas, font=fonte)
    profissao.pack()

    tk.Label(master=etiquetas, text="Área de atuação:", font=fonte).pack()
    area = tk.Entry(master=entradas, font=fonte)
    area.pack()

    tk.Label(master=etiquetas, text="Telefone:", font=fonte).pack()
    telefone = tk.Entry(master=entradas, font=fonte)
    telefone.pack()

    etiquetas.pack(side=tk.LEFT)
    entradas.pack(side=tk.LEFT)
    agl.pack()

    def enviarEntrada():
        entrada = {
            'Nome': nome.get(),
            'CPF': deps.format_cpf(cpf.get()),
            'Profissao': profissao.get(),
            'Atuacao': area.get(),
            'Telefone': telefone.get(),
            'Entrada': None,
            'Saida': None,
            'Confirmado': False,
        }

        deps.finalize_cadastro(caminho, entrada)

    tk.Button(text="Enviar", command=enviarEntrada, font=fonte).pack()

    janela.mainloop()


if __name__ == "__main__":
    entrada("voluntário")
