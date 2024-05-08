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

    tk.Label(master=etiquetas, text="Telefone:", font=fonte).pack()
    telefone = tk.Entry(master=entradas, font=fonte)
    telefone.pack()

    tk.Label(master=etiquetas, text="Profissão:", font=fonte).pack()
    profissao = tk.Entry(master=entradas, font=fonte)
    profissao.pack()

    tk.Label(master=etiquetas, text="Área de atuação:", font=fonte).pack()
    area = tk.Entry(master=entradas, font=fonte)
    area.pack()

    etiquetas.pack(side=tk.LEFT)
    entradas.pack(side=tk.LEFT)
    agl.pack()

    msg = tk.Label(master=janela, font=fonte)
    msg.pack()

    def enviarEntrada(evento):
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

        match deps.finalize_cadastro(caminho, entrada):
            case (True, _):
                msg.config(text="Cadastro registrado", bg="green")
                nome.delete(0, tk.END)
                cpf.delete(0, tk.END)
                cpf.config(bg="white")
                telefone.delete(0, tk.END)
                telefone.config(bg="white")
                area.delete(0, tk.END)
            case (False, erros):
                for erro in erros:
                    match erro:
                        case "cpf": cpf.config(bg="red")
                        case "telefone": telefone.config(bg="red")

    tk.Button(master=janela, text="Enviar",
              command=enviarEntrada, font=fonte).pack()

    janela.bind("<Return>", enviarEntrada)

    janela.mainloop()


if __name__ == "__main__":
    entrada("voluntário")
