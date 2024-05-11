import deps.dependencies as deps

# pergunta no terminal se os dados da pessoa estão corretos
def liberaTerminal(tipo) -> None:
    match (tipo):
        case 'abrigado':
            path = deps.PATH_ABR
        case 'voluntário':
            path = deps.PATH_VOL
        case 'saude':
            path = deps.PATH_SAU
    while True:
        print('\n\n' + 20 * '-')
        print(f'nova liberação de {tipo}')
        cpf_input = input(f'Digite o CPF do {tipo} de saída: ')
        cpf = deps.format_cpf(cpf_input)  # Assuming format_cpf formats correctly

        if cpf_input == '':
            print(
                f'{tipo} Não possui Cadastro com CPF. Necessita de atualização manual.')
            print(f'Horario de saída do {tipo}: ' + deps.time.strftime('%H:%M:%S'))

        elif not deps.validate_cpf(cpf):
            print('CPF inválido. Tente novamente.')
            continue

        match deps.libera(path, cpf):
            case (_, "não encontrado"):
                print(
                    f'CPF {cpf} não encontrado. Saída NÃO autorizada.\nTente novamente.')
                continue
            case (nome, "já saiu"):
                print(f'{nome} já saiu. Saída NÃO autorizada.\nTente novamente.')
                continue
            case (nome, "confirmado"):
                verifica_saida = input(f'Confirma a saída de {nome}? (s/n): ').strip().lower()
                if verifica_saida in ['', 's', 'y', 'sim', 'yes']:
                    print('Saída confirmada')
                    break
                else:
                    print('Saída não confirmada. Retomando início...')
                    # por enquanto isso não faz nada, mas deveria remover o horário de saída da pessoa


# pergunta os dados no terminal e realiza o cadastro de uma pessoa
def cadastroTerminal(tipo) -> None:
    cadastro = {
        'Nome': '',
        'CPF': '',
        'Profissao': '',
        'Atuacao': '',
        'Telefone': '',
        'Entrada': None,
        'Saida': None,
    }

    match (tipo):
        case 'abrigado':
            path = deps.PATH_ABR
        case 'voluntário':
            path = deps.PATH_VOL
        case 'saude':
            path = deps.PATH_SAU
    csv_db = deps.carrega_csv(path)

    while True:
        print('\n\n' + 20 * '-')
        print(f'Novo cadastro de {tipo}')

        cpf_found = False
        phone_found = False

        cadastro = deps.input_cpf(cadastro, tipo)

        cadastro, cpf_found = deps.check_existing_person(csv_db, cadastro, "CPF")
        if cpf_found:
            print("CPF encontrado na base!")
            if deps.confirmacaoTerminal(cadastro):
                deps.finalize_cadastro(path, cadastro)
                continue
        else:
            print("CPF não consta na base, prosseguir com o cadastro")

            cpf = cadastro['CPF']
            cadastro = deps.input_telefone(cadastro, tipo)

            cadastro, phone_found = deps.check_existing_person(
                csv_db, cadastro, "Telefone")
            if phone_found:
                print("Telefone encontrado na base!")
                # Readiciona o CPF digita pois na base esta vazio
                cadastro['CPF'] = cpf
                if deps.confirmacaoTerminal(cadastro):
                    deps.finalize_cadastro(path, cadastro)
                    continue
            else:
                print("Telefone não consta na base, prosseguir com o cadastro")

        if cpf_found:  # If pra nao repetir caso o usuario queira ajustar o cadastro encontrado
            cadastro = deps.input_telefone(cadastro, tipo)

        cadastro['Nome'] = input(f'Nome do {tipo}: ')

        cadastro['Profissao'] = input(f'Profissão do {tipo}: ')
        cadastro['Atuacao'] = input(f'Área de atuação do {tipo}: ')

        if deps.confirmacaoTerminal(cadastro):
            print('Cadastro confirmado. Aguarde enquanto realizamos o cadastro...')
            deps.finalize_cadastro(path, cadastro)
            print('Cadastro realizado com sucesso!\n')
        else:
            print('Dados incorretos. Cadastro cancelado. Reinicie o processo\n\n')