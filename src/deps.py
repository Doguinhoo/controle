import pandas as pd
import re
import time
import os

PATH = './'

PATH_VOL = PATH + 'Voluntarios/voluntarios.csv'
PATH_REF = PATH + 'Abrigados/abrigados.csv'


def create_empty_csv(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df = pd.DataFrame(columns=[
        'Nome',
        'CPF',
        'Profissao',
        'Atuacao',
        'Telefone',
        'Data',
        'HoraEntrada',
        'HoraSaida',
        'Confirmado'
    ]
    )

    df.to_csv(path)


def check_row_using_cpf(path, cpf) -> pd.DataFrame:
    if not os.path.exists(path):
        create_empty_csv(path)
        return pd.DataFrame()
    else:
        df = pd.read_csv(path, sep=';', dtype={'CPF': str})
    df['CPF'] = df['CPF'].str.strip()  # Clean any whitespace
    match = df[df['CPF'] == cpf]
    if not match.empty:
        return match.iloc[[-1]]
    return match


def get_name(df, index):
    return df.loc[index, 'Nome'] if not df.empty else ''


# pergunta um cpf para liberação pelo terminal e o retorna
def liberaTerminal(path, tipo):
    while True:
        print('\n\n' + 20 * '-')
        print(f'nova liberação de {tipo}')
        cpf_input = input(f'Digite o CPF do {tipo} de saída: ')
        cpf = format_cpf(cpf_input)  # Assuming format_cpf formats correctly

        if cpf_input == '':
            print(
                f'{tipo} Não possui Cadastro com CPF. Necessita de atualização manual.')
            print(f'Horario de saída do {tipo}: ' + time.strftime('%H:%M:%S'))

        elif not validate_cpf(cpf):
            print('CPF inválido. Tente novamente.')
            continue

        match libera(path, cpf):
            case (_, "não encontrado"):
                print(
                    f'CPF {cpf} não encontrado. Saída NÃO autorizada.\nTente novamente.')
                continue
            case (nome, "já saiu"):
                print(f'{nome} já saiu. Saída NÃO autorizada.\nTente novamente.')
                continue
            case (nome, "confirmado"):
                verifica_saida = input(f'Confirma a saída de {
                                       nome}? (s/n): ').strip().lower()
                if verifica_saida in ['', 's', 'y', 'sim', 'yes']:
                    print('Saída confirmada')
                    break
                else:
                    print('Saída não confirmada. Retomando início...')
                    # por enquanto isso não faz nada, mas deveria remover o horário de saída da pessoa


# tenta diberar a pessoa com o cpf recebido, retorna o nome da pessoa e o resultado da tentativa
def libera(path, cpf):
    resultado_df = check_row_using_cpf(path, cpf)
    if resultado_df.empty:
        return (None, "não encontrado")

    nome = get_name(resultado_df, resultado_df.index[0])

    if resultado_df['HoraSaida'].notnull().all():
        return (nome, "já saiu")

    df = pd.read_csv(path, sep=';')
    # Setting an item of incompatible dtype is deprecated and will raise an error in a future version of pandas. Value '15:47:54' has dtype incompatible with float64, please explicitly cast to a compatible dtype first.
    df.loc[resultado_df.index[0], 'HoraSaida'] = time.strftime('%H:%M:%S')
    df.to_csv(path, sep=';', index=False)
    return (nome, "confirmado")


def format_cpf(cpf: str):
    return cpf[:3] + '.' + cpf[3:6] + '.' + cpf[6:9] + '-' + cpf[9:11]


def validate_cpf(cpf: str) -> bool:
    """ Efetua a validação do CPF, tanto formatação quando dígito verificadores.

    Parâmetros:
        cpf (str): CPF a ser validado

    Retorno:
        bool:
            - Falso, quando o CPF não possuir o formato 999.999.999-99;
            - Falso, quando o CPF não possuir 11 caracteres numéricos;
            - Falso, quando os dígitos verificadores forem inválidos;
            - Verdadeiro, caso contrário.

    Exemplos:

    >>> validate('529.982.247-25')
    True
    >>> validate('52998224725')
    False
    >>> validate('111.111.111-11')
    False
    """

    # Verifica a formatação do CPF
    if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        return False

    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais:
    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False

    return True


def serializaCadastro(caminho, cadastro: dict):
    df = pd.read_csv(caminho, sep=';')
    new_row = pd.DataFrame([cadastro.values()], columns=cadastro.keys())
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(caminho, index=False, sep=';')


def validaTelefone(telefone: str) -> bool:
    return telefone.isdigit() and len(telefone) == 11


# pergunta no terminal se os dados da pessoa estão corretos
def confirmacaoTerminal(cadastro):
    print(f'''
Verifique se as informações estão corretas:
Nome: {cadastro['Nome']}
CPF: {cadastro['CPF']}
Profissão: {cadastro['Profissao']}
Área de atuação: {cadastro['Atuacao']}
Telefone: {cadastro['Telefone']}
Confirma? (s/n): ''')
    resposta = input().strip().lower()
    return resposta in ['s', 'sim', 'yes', 'y', '']


# pergunta os dados no terminal e realiza o cadastro de uma pessoa
def cadastroTerminal(caminho, tipo):
    cadastro = {
        'Nome': '',
        'CPF': '',
        'Profissao': '',
        'Atuacao': '',
        'Telefone': '',
        'Data': None,
        'HoraEntrada': None,
        'HoraSaida': None,
        'Confirmado': False,
    }

    while not cadastro['Confirmado']:
        print('\n\n' + 20 * '-')
        print(f'Novo cadastro de {tipo}')
        cadastro['Nome'] = input(f'Nome do {tipo}: ')

        cpf = input(f'CPF do {tipo}: ')
        if cpf != '':
            cadastro['CPF'] = format_cpf(cpf)
            while not validate_cpf(cadastro['CPF']):
                print('CPF inválido')
                cadastro['CPF'] = format_cpf(
                    input(f'Reenvie CPF do {tipo}: '))
        else:
            cadastro['CPF'] = cpf

        cadastro['Profissao'] = input(f'Profissão do {tipo}: ')
        cadastro['Atuacao'] = input(f'Área de atuação do {tipo}: ')

        cadastro['Telefone'] = input(f'Telefone do {tipo}: ')
        while not validaTelefone(cadastro['Telefone']):
            print('Telefone inválido')
            cadastro['Telefone'] = input(f'Reenvie telefone do {tipo}: ')

        cadastro['Confirmado'] = confirmacaoTerminal(cadastro)
        if cadastro['Confirmado']:
            print('Cadastro confirmado. Aguarde enquanto realizamos o cadastro...')
            cadastro['Data'] = time.strftime('%d/%m/%Y')
            cadastro['HoraEntrada'] = time.strftime('%H:%M:%S')

            serializaCadastro(caminho, cadastro)

            print('Cadastro realizado com sucesso!\n')
        else:
            print('Dados incorretos. Cadastro cancelado. Reinicie o processo\n\n')
