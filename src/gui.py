import tkinter as tk
import deps

# tipo: "voluntário" ou "abrigado"
tamanhoFonte = 28


def entrada(tipo):
    match tipo:
        case 'voluntário': caminho = deps.PATH_VOL
        case 'abrigado': caminho = deps.PATH_ABR

    janela = tk.Tk()
    janela.resizable(False, False)
    janela.option_add('*Font', 'TkDefaultFont 20')
    janela.title(f"Entrada de {tipo}")

    grade = tk.Frame(master=janela)

    tk.Label(master=grade, text="Nome:").grid(row=0, column=0)
    nome = tk.Entry(master=grade, width=50)
    nome.grid(row=0, column=1)

    tk.Label(master=grade, text="CPF:").grid(row=1, column=0)
    cpf = tk.Entry(master=grade, width=50)
    cpf.grid(row=1, column=1)

    tk.Label(master=grade, text="Telefone:").grid(row=2, column=0)
    telefone = tk.Entry(master=grade, width=50)
    telefone.grid(row=2, column=1)

    tk.Label(master=grade, text="Profissão:").grid(row=3, column=0)
    profissao = tk.Entry(master=grade, width=50)
    profissao.grid(row=3, column=1)

    tk.Label(master=grade, text="Área de atuação:").grid(row=4, column=0)
    area = tk.Entry(master=grade, width=50)
    area.grid(row=4, column=1)

    grade.pack()

    msg = tk.Label(master=janela, wraplength=350)
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
        }

        match deps.finalize_cadastro(caminho, entrada):
            case (True, _):
                msg.config(text="Cadastro registrado", bg="green")
                nome.delete(0, tk.END)
                cpf.delete(0, tk.END)
                cpf.config(bg="white")
                telefone.delete(0, tk.END)
                telefone.config(bg="white")
                profissao.delete(0, tk.END)
                area.delete(0, tk.END)
            case (False, erros):
                for erro in erros:
                    match erro:
                        case "cpf": cpf.config(bg="red")
                        case "telefone": telefone.config(bg="red")

    tk.Button(master=janela, text="Enviar",
              command=lambda: enviarEntrada(None)).pack()

    janela.bind("<Return>", enviarEntrada)

    janela.mainloop()


def saida(tipo):
    match tipo:
        case 'voluntário': caminho = deps.PATH_VOL
        case 'abrigado': caminho = deps.PATH_ABR

    janela = tk.Tk()
    janela.option_add('*Font', 'TkDefaultFont 20')
    janela.resizable(False, False)

    janela.title(f"Saída de {tipo}")

    grade = tk.Frame(master=janela)

    tk.Label(master=grade, text="CPF:").grid(row=0, column=0)
    cpf = tk.Entry(master=grade)
    cpf.grid(row=0, column=1)

    grade.pack()

    msg = tk.Label(master=janela, wraplength=350)
    msg.pack()

    def enviarSaida(evento):
        match deps.libera(caminho, deps.format_cpf(cpf.get())):
            case (_, "não encontrado"):
                msg.config(text=f"{tipo} não encontrado", bg="red")
            case (nome, "já saiu"):
                msg.config(text=f"{nome} já saiu", bg="red")
            case (nome, "confirmado"):
                msg.config(text=f"Saída de {
                           nome} marcada com sucesso", bg="green")
                cpf.delete(0, tk.END)

    tk.Button(master=janela, text="Enviar",
              command=lambda: enviarSaida(None)).pack()

    janela.bind("<Return>", enviarSaida)

    janela.mainloop()


def janelaDeControle(tipo):
    janela = tk.Tk()
    janela.resizable(False, False)
    janela.option_add('*Font', 'TkDefaultFont 40')
    janela.title(f"Controde de {tipo}")

    # fonte = font.Font(size=tamanhoFonte)
    grade = tk.Frame(master=janela)

    tk.Button(master=grade, text="Entrada",
              command=lambda: entrada(tipo)).grid(row=0, column=0)
    tk.Button(master=grade, text="Saída",
              command=lambda: saida(tipo)).grid(row=0, column=1)

    grade.pack()

    janela.mainloop()


if __name__ == "__main__":
    janelaDeControle("voluntário")
