import pandas as pd
import re
import time
import os

PATH = './'

PATH_VOL = PATH + 'Voluntarios/voluntarios.csv'
PATH_REF = PATH + 'Abrigados/abrigados.csv'

def create__empty_csv(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df = pd.DataFrame(columns=[
            'Nome',
            'CPF',
            'Profissao',
            'Atuacao',
            'Telefone',
            'Entrada',
            'Saida',
            'Confirmado'
            ]
            )

        df.to_csv(path)

def check_row_using_cpf(path, cpf) -> pd.DataFrame:
    if not os.path.exists(path):
        create__empty_csv(path)
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


def liberate(path, type):
    print(f'SAÍDA DE {type.upper()}')
    while True:
        print('\n\n' + 20 * '-')
        print(f'nova liberação de {type}')
        cpf_input = input(f'Digite o CPF do {type} de saída: ')
        CPF = format_cpf(cpf_input)  # Assuming format_cpf formats correctly

        if cpf_input == '':
            print(f'{type} Não possui Cadastro com CPF. Necessita de atualização manual.')
            print(f'Horario de saída do {type}: ' + time.strftime('%H:%M:%S'))

        elif not validate_cpf(CPF):
            print('CPF inválido. Tente novamente.')
            continue

        result_df = check_row_using_cpf(path, CPF)
        if result_df.empty:
            print(f'CPF {CPF} não encontrado. Saída NÃO autorizada.\nTente novamente.')
            continue

        if result_df['Saida'].notnull().all():
            print(f'{get_name(result_df, result_df.index[0])} já saiu. Saída NÃO autorizada.\nTente novamente.')
            continue
        name = get_name(result_df, result_df.index[0])
        verify_exit = input(f'Confirma a saída de {name}? (s/n): ').strip().lower()
        if verify_exit in ['', 's', 'y', 'sim', 'yes']:
            df = pd.read_csv(path, sep=';')
            df.loc[result_df.index[0], 'Saida'] = time.strftime('%d/%m/%Y %H:%M:%S') #Setting an item of incompatible dtype is deprecated and will raise an error in a future version of pandas. Value '15:47:54' has dtype incompatible with float64, please explicitly cast to a compatible dtype first.
            df.to_csv(path, sep=';', index=False)
            print('Saída confirmada')
        else:
            print('Saída não confirmada. Retomando início...')


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


def add_row_csv(path, row: dict):
    df = pd.read_csv(path, sep=';')
    new_row = pd.DataFrame([row.values()], columns=row.keys())
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(path, index=False, sep=';')


def add_unique_row_csv(path, row):
    if check_row_using_cpf(path, row['CPF']).empty:
        add_row_csv(path, row)
        print("Registro adicionado com sucesso.")
    else:
        print("Erro: CPF já registrado.")


def validate_telefone(telefone: str) -> bool:
    return telefone.isdigit() and len(telefone) == 11


def confirmacao(cadastro):
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


def cadastro(path, type):
    while True:
        cadastro = {
            'Nome': '',
            'CPF': '',
            'Profissao': '',
            'Atuacao': '',
            'Telefone': '',
            'Entrada': None,
            'Saida': None,
            'Confirmado': False,
        }
        print(f'Cadastro de {type.upper()}')
        while not cadastro['Confirmado']:
            print('\n\n' + 20 * '-')
            print(f'Novo cadastro de {type}')
            cadastro['Nome'] = input(f'Nome do {type}: ')

            cpf = input(f'CPF do {type}: ')
            if cpf != '':
                cadastro['CPF'] = format_cpf(cpf)
                while not validate_cpf(cadastro['CPF']):
                    print('CPF inválido')
                    cadastro['CPF'] = format_cpf(
                        input(f'Reenvie CPF do {type}: '))
            else:
                cadastro['CPF'] = cpf

            cadastro['Profissao'] = input(f'Profissão do {type}: ')
            cadastro['Atuacao'] = input(f'Área de atuação do {type}: ')

            cadastro['Telefone'] = input(f'Telefone do {type}: ')
            while not validate_telefone(cadastro['Telefone']):
                print('Telefone inválido')
                cadastro['Telefone'] = input(f'Reenvie telefone do {type}: ')

            cadastro['Confirmado'] = confirmacao(cadastro)
            if cadastro['Confirmado']:
                print('Cadastro confirmado. Aguarde enquanto realizamos o cadastro...')
                cadastro['Entrada'] = time.strftime('%d/%m/%Y %H:%M:%S')

                add_unique_row_csv(path, cadastro)
                # Cadastro: \n', cadastro)
                print('Cadastro realizado com sucesso!\n')
                continue
            print('Dados incorretos. Cadastro cancelado. Reinicie o processo\n\n')
