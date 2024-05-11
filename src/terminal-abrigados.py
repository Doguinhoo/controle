from deps.main import cadastroTerminal, liberaTerminal

TYPE = 'voluntário'
if __name__ == '__main__':

    print(f'Sistema para {TYPE}s')
    user_input = input('Cadastro ou Baixa? (C/B)')

    if user_input.upper() == 'C':
        print(f'CADASTRO DE {TYPE.upper()}')
        while True:
            cadastroTerminal(TYPE)

    if user_input.upper() == 'B':
        print(f'SAÍDA DE {TYPE.upper()}')
        while True:
            liberaTerminal(TYPE)
