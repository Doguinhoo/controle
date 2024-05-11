from deps.main import cadastroTerminal, liberaTerminal
from deps.dependencies import PATH_ABR as PATH

if __name__ == '__main__':
    type = 'abrigado'

    print(f'Sistema para {type}s')
    user_input = input('Cadastro ou Baixa? (C/B)')

    if user_input.upper() == 'C':
        print(f'CADASTRO DE {type.upper()}')
        while True:
            cadastroTerminal(PATH, type)

    if user_input.upper() == 'B':
        print(f'SAÍDA DE {type.upper()}')
        while True:
            liberaTerminal(type)
