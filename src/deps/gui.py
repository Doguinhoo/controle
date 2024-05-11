import tkinter as tk
from deps.dependencies import *

# tipo: "voluntário", "abrigado" ou "voluntário da saúde"
FONT_SIZE = 28


def entrada_saude(tipo) -> None:
    caminho = PATH_SAU

    def testaCpf() -> bool:

        entrada = {
            'Nome': nome.get(),
            'CPF': format_cpf(cpf.get()),
            'Registro': reg_conselho.get(),
            'Sala': sala.get(),
            'Entrada': '',
            'Saida': '',
        }

        csv_db = carrega_csv(caminho)

        match check_existing_person(csv_db, entrada, "CPF", False):
            case (entrada, True):
                nome.delete(1, tk.END)
                nome.insert(0, entrada['Nome'])
                reg_conselho.delete(0, tk.END)
                reg_conselho.insert(0, entrada['Registro'])
                sala.delete(0, tk.END)
                sala.insert(0, entrada['Sala'])
                return True
            case (_, False):
                return False

    janela = tk.Tk()
    janela.resizable(False, False)
    janela.option_add('*Font', 'TkDefaultFont 20')
    janela.title(f"Entrada de {tipo}")

    grade = tk.Frame(master=janela)

    tk.Label(master=grade, text="CPF:").grid(row=0, column=0)
    cpf = tk.Entry(master=grade, width=50, validate="focusout", validatecommand=testaCpf)
    cpf.grid(row=0, column=1)

    tk.Label(master=grade, text="Nome:").grid(row=1, column=0)
    nome = tk.Entry(master=grade, width=50)
    nome.grid(row=1, column=1)

    tk.Label(master=grade, text="Registro do Conselho:").grid(row=2, column=0)
    reg_conselho = tk.Entry(master=grade, width=50)
    reg_conselho.grid(row=2, column=1)

    tk.Label(master=grade, text="Sala:").grid(row=3, column=0)
    sala = tk.Entry(master=grade, width=50)
    sala.grid(row=3, column=1)

    grade.pack()

    msg = tk.Label(master=janela, wraplength=350)
    msg.pack()

    def enviarEntrada_saude(evento) -> None:
        entrada = {
            'Nome': nome.get(),
            'CPF': format_cpf(cpf.get()),
            'Registro' : reg_conselho.get(),
            'Sala' : sala.get(),
            'Entrada': '',
            'Saida': '',
        }

        match finalize_cadastro(caminho, entrada):
            case (True, _):
                msg.config(text="Cadastro registrado", bg="green")
                cpf.delete(0, tk.END)
                cpf.config(bg="white")
                nome.delete(0, tk.END)
                reg_conselho.delete(0, tk.END)
                sala.delete(0, tk.END)
            case (False, erros):
                for erro in erros:
                    match erro:
                        case "cpf": cpf.config(bg="red")

    tk.Button(master=janela, text="Enviar",
              command=lambda: enviarEntrada_saude(None)).pack()

    janela.bind("<Return>", enviarEntrada_saude)
    janela.bind("<KP_Enter>", enviarEntrada_saude)
    janela.bind("<Escape>", lambda _: janela.destroy())

    cpf.focus_set()

    janela.mainloop()


def saida_saude(tipo) -> None:
    match tipo:
        case 'voluntário da saude': caminho = PATH_SAU
        case _: caminho = PATH_UNKNOWN
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

    def enviarSaida(evento) -> None:
        match libera(caminho, format_cpf(cpf.get())):
            case (_, "CPF inválido"):
                msg.config(text=f"CPF do {tipo} inválido", bg="red")
            case (_, "não encontrado"):
                msg.config(text=f"{tipo} não encontrado", bg="red")
            case (nome, "já saiu"):
                msg.config(text=f"{nome} já saiu", bg="red")
            case (nome, "confirmado"):
                msg.config(text=f"Saída de {nome} marcada com sucesso", bg="green")
                cpf.delete(0, tk.END)

    tk.Button(master=janela, text="Enviar",
              command=lambda: enviarSaida(None)).pack()

    janela.bind("<Return>", enviarSaida)
    janela.bind("<KP_Enter>", enviarSaida)
    janela.bind("<Escape>", lambda _: janela.destroy())

    cpf.focus_set()

    janela.mainloop()


def entrada(tipo) -> None:
    def testaCpf() -> bool:
        entrada = {
            'Nome': nome.get(),
            'CPF': format_cpf(cpf.get()),
            'Profissao': profissao.get(),
            'Atuacao': area.get(),
            'Telefone': telefone.get(),
            'Entrada': '',
            'Saida': '',
        }

        csv_db = carrega_csv(caminho)

        match check_existing_person(csv_db, entrada, "CPF"):
            case (entrada, True):
                nome.delete(1, tk.END)
                nome.insert(0, entrada['Nome'])
                telefone.delete(0, tk.END)
                telefone.insert(0, entrada['Telefone'])
                profissao.delete(0, tk.END)
                profissao.insert(0, entrada['Profissao'])
                area.delete(0, tk.END)
                area.insert(0, entrada['Atuacao'])
                return True
            case (_, False):
                return False

    match tipo:
        case 'voluntário': caminho = PATH_VOL
        case 'abrigado': caminho = PATH_ABR

    janela = tk.Tk()
    janela.resizable(False, False)
    janela.option_add('*Font', 'TkDefaultFont 20')
    janela.title(f"Entrada de {tipo}")

    grade = tk.Frame(master=janela)

    tk.Label(master=grade, text="CPF:").grid(row=0, column=0)
    cpf = tk.Entry(master=grade, width=50, validate="focusout", validatecommand=testaCpf)
    cpf.grid(row=0, column=1)

    tk.Label(master=grade, text="Nome:").grid(row=1, column=0)
    nome = tk.Entry(master=grade, width=50)
    nome.grid(row=1, column=1)

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

    def enviarEntrada(evento) -> None:
        entrada = {
            'Nome': nome.get(),
            'CPF': format_cpf(cpf.get()),
            'Profissao': profissao.get(),
            'Atuacao': area.get(),
            'Telefone': telefone.get(),
            'Entrada': '',
            'Saida': '',
        }

        match finalize_cadastro(caminho, entrada):
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
    janela.bind("<KP_Enter>", enviarEntrada)
    janela.bind("<Escape>", lambda _: janela.destroy())

    cpf.focus_set()

    janela.mainloop()


def saida(tipo) -> None:
    match tipo:
        case 'voluntário': caminho = PATH_VOL
        case 'abrigado': caminho = PATH_ABR

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

    def enviarSaida(evento) -> None:
        match libera(caminho, format_cpf(cpf.get())):
            case (_, "CPF inválido"):
                msg.config(text=f"CPF do {tipo} inválido", bg="red")
            case (_, "não encontrado"):
                msg.config(text=f"{tipo} não encontrado", bg="red")
            case (nome, "já saiu"):
                msg.config(text=f"{nome} já saiu", bg="red")
            case (nome, "confirmado"):
                msg.config(text=f"Saída de {nome} marcada com sucesso", bg="green")
                cpf.delete(0, tk.END)

    tk.Button(master=janela, text="Enviar",
              command=lambda: enviarSaida(None)).pack()

    janela.bind("<Return>", enviarSaida)
    janela.bind("<KP_Enter>", enviarSaida)
    janela.bind("<Escape>", lambda _: janela.destroy())

    cpf.focus_set()

    janela.mainloop()


def janelaDeControle(tipo) -> None:
    janela = tk.Tk()
    janela.resizable(False, False)
    janela.option_add('*Font', 'TkDefaultFont 40')
    janela.title(f"Controde de {tipo}")

    grade = tk.Frame(master=janela)

    match tipo:
        case 'voluntário da saude':
            botaoEntrada = tk.Button(master=grade, text="Entrada", command=lambda: entrada_saude(tipo))
            botaoEntrada.grid(row=0, column=0)
            botaoSaida = tk.Button(master=grade, text="Saída", command=lambda: saida_saude(tipo))
            botaoSaida.grid(row=0, column=1)
        case _:
            botaoEntrada = tk.Button(master=grade, text="Entrada", command=lambda: entrada(tipo))
            botaoEntrada.grid(row=0, column=0)
            botaoSaida = tk.Button(master=grade, text="Saída", command=lambda: saida(tipo))
            botaoSaida.grid(row=0, column=1)
    grade.pack()

    janela.bind('<Return>', lambda _: janela.focus_get().invoke())
    janela.bind('<KP_Enter>', lambda _: janela.focus_get().invoke())
    janela.bind("<Escape>", lambda _: janela.destroy())

    botaoEntrada.focus_set()

    janela.mainloop()
