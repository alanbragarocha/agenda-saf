#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface simples para editar os dados da agenda
"""

import json
import sys


def carregar_dados(arquivo='agenda_data.json'):
    """Carrega os dados do arquivo JSON"""
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo '{arquivo}' não encontrado!")
        return None
    except json.JSONDecodeError as e:
        print(f"Erro ao ler JSON: {e}")
        return None


def salvar_dados(dados, arquivo='agenda_data.json'):
    """Salva os dados no arquivo JSON"""
    try:
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        print(f"✓ Dados salvos em '{arquivo}'")
        return True
    except Exception as e:
        print(f"Erro ao salvar: {e}")
        return False


def editar_membro_diretoria(dados):
    """Edita um membro da diretoria"""
    print("\n=== EDITAR DIRETORIA ===")
    for i, membro in enumerate(dados['diretoria'], 1):
        print(f"{i}. {membro['cargo']}: {membro['nome']}")
    print("0. Adicionar novo membro")

    try:
        escolha = int(
            input(
                "\nEscolha o número do membro para editar (0 para adicionar, -1 para cancelar): "
            )
        )
        if escolha == -1:
            return

        if escolha == 0:
            # Adicionar novo membro
            cargo = input("Cargo: ").strip()
            nome = input("Nome: ").strip()
            data_nasc = input("Data de nascimento (DD/MM): ").strip()
            email = input("Email (opcional): ").strip()
            endereco = input("Endereço (opcional): ").strip()

            novo_membro = {"cargo": cargo, "nome": nome, "data_nascimento": data_nasc}
            if email:
                novo_membro["email"] = email
            if endereco:
                novo_membro["endereco"] = endereco

            dados['diretoria'].append(novo_membro)
            print("✓ Novo membro adicionado!")
            return

        idx = escolha - 1
        if idx < 0 or idx >= len(dados['diretoria']):
            return

        membro = dados['diretoria'][idx]
        print(f"\nEditando: {membro['cargo']}")

        # Editar cargo
        print(f"Cargo atual: {membro['cargo']}")
        novo_cargo = input("Novo cargo (Enter para manter): ").strip()
        if novo_cargo:
            membro['cargo'] = novo_cargo

        # Editar nome
        print(f"Nome atual: {membro['nome']}")
        novo_nome = input("Novo nome (Enter para manter): ").strip()
        if novo_nome:
            membro['nome'] = novo_nome

        # Editar data de nascimento
        print(f"Data de nascimento atual: {membro.get('data_nascimento', '')}")
        nova_data = input("Nova data (DD/MM, Enter para manter): ").strip()
        if nova_data:
            membro['data_nascimento'] = nova_data

        # Editar email
        print(f"Email atual: {membro.get('email', '')}")
        novo_email = input(
            "Novo email (Enter para manter, 'remover' para remover): "
        ).strip()
        if novo_email:
            if novo_email.lower() == 'remover':
                membro.pop('email', None)
            else:
                membro['email'] = novo_email

        # Editar endereço
        print(f"Endereço atual: {membro.get('endereco', '')}")
        novo_endereco = input(
            "Novo endereço (Enter para manter, 'remover' para remover): "
        ).strip()
        if novo_endereco:
            if novo_endereco.lower() == 'remover':
                membro.pop('endereco', None)
            else:
                membro['endereco'] = novo_endereco

        # Opção de remover
        remover = input("\nDeseja remover este membro? (s/N): ").strip().lower()
        if remover == 's':
            dados['diretoria'].pop(idx)
            print("✓ Membro removido!")
        else:
            print("✓ Membro atualizado!")

    except (ValueError, KeyboardInterrupt):
        print("Operação cancelada.")


def editar_saf(dados):
    """Edita uma SAF"""
    print("\n=== EDITAR SAF ===")
    for saf in dados['safs']:
        print(f"{saf['numero']}. {saf['nome']}")
    print("0. Adicionar nova SAF")

    try:
        escolha = int(
            input(
                "\nEscolha o número da SAF para editar (0 para adicionar, -1 para cancelar): "
            )
        )
        if escolha == -1:
            return

        if escolha == 0:
            # Adicionar nova SAF
            num = len(dados['safs']) + 1
            nome = input("Nome da SAF: ").strip()
            endereco = input("Endereço da igreja: ").strip()

            print("\n--- Dados do Pastor ---")
            pastor_nome = input("Nome do pastor: ").strip()
            pastor_data = input("Data de nascimento do pastor (DD/MM): ").strip()

            print("\n--- Dados do Presidente ---")
            pres_nome = input("Nome do presidente: ").strip()
            pres_data = input("Data de nascimento (DD/MM): ").strip()
            pres_endereco = input("Endereço: ").strip()
            pres_cep = input("CEP: ").strip()
            pres_tel = input("Telefone: ").strip()
            pres_email = input("Email (opcional): ").strip()

            print("\n--- Dados do Conselheiro ---")
            cons_nome = input("Nome do conselheiro (opcional): ").strip()
            cons_data = input("Data de nascimento (DD/MM, opcional): ").strip()

            print("\n--- Aniversário da SAF ---")
            aniv_data = input("Data do aniversário (DD/MM): ").strip()
            aniv_anos = input("Quantos anos: ").strip()

            nova_saf = {
                "numero": num,
                "nome": nome,
                "endereco": endereco,
                "pastor": {"nome": pastor_nome, "data_nascimento": pastor_data},
                "presidente": {
                    "nome": pres_nome,
                    "data_nascimento": pres_data,
                    "endereco": pres_endereco,
                    "cep": pres_cep,
                    "telefone": pres_tel,
                },
                "conselheiro": {"nome": cons_nome, "data_nascimento": cons_data},
                "aniversario": {
                    "data": aniv_data,
                    "anos": int(aniv_anos) if aniv_anos.isdigit() else 0,
                },
            }
            if pres_email:
                nova_saf['presidente']['email'] = pres_email

            dados['safs'].append(nova_saf)
            print("✓ Nova SAF adicionada!")
            return

        saf = next((s for s in dados['safs'] if s['numero'] == escolha), None)
        if not saf:
            print("SAF não encontrada!")
            return

        print(f"\nEditando: {saf['nome']}")

        # Editar nome da SAF
        print(f"Nome atual: {saf['nome']}")
        novo_nome = input("Novo nome (Enter para manter): ").strip()
        if novo_nome:
            saf['nome'] = novo_nome

        # Editar endereço da igreja
        print(f"Endereço atual: {saf.get('endereco', '')}")
        novo_endereco = input("Novo endereço (Enter para manter): ").strip()
        if novo_endereco:
            saf['endereco'] = novo_endereco

        # Editar pastor
        if saf.get('pastor'):
            print(f"\n--- Pastor ---")
            print(f"Nome: {saf['pastor'].get('nome', '')}")
            novo_pastor = input("Novo nome (Enter para manter): ").strip()
            if novo_pastor:
                saf['pastor']['nome'] = novo_pastor

            print(f"Data nascimento: {saf['pastor'].get('data_nascimento', '')}")
            nova_data_pastor = input("Nova data (DD/MM, Enter para manter): ").strip()
            if nova_data_pastor:
                saf['pastor']['data_nascimento'] = nova_data_pastor

        # Editar presidente
        if saf.get('presidente'):
            pres = saf['presidente']
            print(f"\n--- Presidente ---")
            print(f"Nome: {pres.get('nome', '')}")
            novo_nome_pres = input("Novo nome (Enter para manter): ").strip()
            if novo_nome_pres:
                pres['nome'] = novo_nome_pres

            print(f"Data nascimento: {pres.get('data_nascimento', '')}")
            nova_data_pres = input("Nova data (DD/MM, Enter para manter): ").strip()
            if nova_data_pres:
                pres['data_nascimento'] = nova_data_pres

            print(f"Endereço: {pres.get('endereco', '')}")
            novo_end_pres = input("Novo endereço (Enter para manter): ").strip()
            if novo_end_pres:
                pres['endereco'] = novo_end_pres

            print(f"CEP: {pres.get('cep', '')}")
            novo_cep = input("Novo CEP (Enter para manter): ").strip()
            if novo_cep:
                pres['cep'] = novo_cep

            print(f"Telefone: {pres.get('telefone', '')}")
            novo_tel = input("Novo telefone (Enter para manter): ").strip()
            if novo_tel:
                pres['telefone'] = novo_tel

            print(f"Email: {pres.get('email', '')}")
            novo_email = input(
                "Novo email (Enter para manter, 'remover' para remover): "
            ).strip()
            if novo_email:
                if novo_email.lower() == 'remover':
                    pres.pop('email', None)
                else:
                    pres['email'] = novo_email

        # Editar conselheiro
        if saf.get('conselheiro'):
            cons = saf['conselheiro']
            print(f"\n--- Conselheiro ---")
            print(f"Nome: {cons.get('nome', '')}")
            novo_nome_cons = input("Novo nome (Enter para manter): ").strip()
            if novo_nome_cons:
                cons['nome'] = novo_nome_cons

            print(f"Data nascimento: {cons.get('data_nascimento', '')}")
            nova_data_cons = input("Nova data (DD/MM, Enter para manter): ").strip()
            if nova_data_cons:
                cons['data_nascimento'] = nova_data_cons

        # Editar aniversário
        if saf.get('aniversario'):
            aniv = saf['aniversario']
            print(f"\n--- Aniversário ---")
            print(f"Data: {aniv.get('data', '')}")
            nova_data_aniv = input("Nova data (DD/MM, Enter para manter): ").strip()
            if nova_data_aniv:
                aniv['data'] = nova_data_aniv

            print(f"Anos: {aniv.get('anos', '')}")
            novos_anos = input("Novos anos (Enter para manter): ").strip()
            if novos_anos and novos_anos.isdigit():
                aniv['anos'] = int(novos_anos)

        # Opção de remover
        remover = input("\nDeseja remover esta SAF? (s/N): ").strip().lower()
        if remover == 's':
            dados['safs'] = [s for s in dados['safs'] if s['numero'] != escolha]
            # Renumerar SAFs
            for i, s in enumerate(dados['safs'], 1):
                s['numero'] = i
            print("✓ SAF removida!")
        else:
            print("✓ SAF atualizada!")

    except (ValueError, KeyboardInterrupt):
        print("Operação cancelada.")


def gerenciar_atividades_realizadas(dados):
    """Gerencia atividades realizadas"""
    print("\n=== GERENCIAR ATIVIDADES REALIZADAS ===")

    if 'atividades_realizadas_2023' not in dados:
        dados['atividades_realizadas_2023'] = []

    atividades = dados['atividades_realizadas_2023']

    print("1. Adicionar atividade realizada")
    print("2. Editar atividade realizada")
    print("3. Remover atividade realizada")
    print("4. Listar todas as atividades realizadas")
    print("0. Voltar")

    try:
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == '1':
            # Adicionar
            data = input("Data da atividade (DD/MM, opcional): ").strip()
            descricao = input("Descrição da atividade: ").strip()

            if descricao:
                nova_atividade = {"data": data, "descricao": descricao}
                atividades.append(nova_atividade)
                print("✓ Atividade adicionada!")

        elif opcao == '2' or opcao == '3':
            # Editar ou remover
            if not atividades:
                print("Nenhuma atividade registrada!")
                return

            print("\nAtividades realizadas:")
            for i, ativ in enumerate(atividades, 1):
                data_str = f"{ativ['data']} – " if ativ.get('data') else ""
                print(f"{i}. {data_str}{ativ['descricao']}")

            ativ_idx = int(input("\nEscolha o número da atividade: ")) - 1
            if ativ_idx < 0 or ativ_idx >= len(atividades):
                return

            if opcao == '3':
                # Remover
                atividades.pop(ativ_idx)
                print("✓ Atividade removida!")
            else:
                # Editar
                ativ = atividades[ativ_idx]
                print(f"\nData atual: {ativ.get('data', '')}")
                nova_data = input("Nova data (Enter para manter): ").strip()
                if nova_data:
                    ativ['data'] = nova_data

                print(f"Descrição atual: {ativ['descricao']}")
                nova_desc = input("Nova descrição (Enter para manter): ").strip()
                if nova_desc:
                    ativ['descricao'] = nova_desc

                print("✓ Atividade atualizada!")

        elif opcao == '4':
            # Listar todas
            print("\n=== TODAS AS ATIVIDADES REALIZADAS ===")
            if atividades:
                for ativ in atividades:
                    data_str = f"{ativ['data']} – " if ativ.get('data') else ""
                    print(f"  • {data_str}{ativ['descricao']}")
            else:
                print("Nenhuma atividade registrada.")
            input("\nPressione Enter para continuar...")

    except (ValueError, KeyboardInterrupt):
        print("Operação cancelada.")


def gerenciar_atividades(dados):
    """Gerencia atividades planejadas"""
    print("\n=== GERENCIAR ATIVIDADES PLANEJADAS ===")
    meses = [
        'janeiro',
        'fevereiro',
        'marco',
        'abril',
        'maio',
        'junho',
        'julho',
        'agosto',
        'setembro',
        'outubro',
        'novembro',
        'dezembro',
    ]

    meses_nomes = {
        'janeiro': 'Janeiro',
        'fevereiro': 'Fevereiro',
        'marco': 'Março',
        'abril': 'Abril',
        'maio': 'Maio',
        'junho': 'Junho',
        'julho': 'Julho',
        'agosto': 'Agosto',
        'setembro': 'Setembro',
        'outubro': 'Outubro',
        'novembro': 'Novembro',
        'dezembro': 'Dezembro',
    }

    print("1. Adicionar atividade")
    print("2. Editar atividade")
    print("3. Remover atividade")
    print("4. Listar todas as atividades")
    print("0. Voltar")

    try:
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == '1':
            # Adicionar
            print("\nMeses disponíveis:")
            for i, mes in enumerate(meses, 1):
                print(f"{i}. {meses_nomes[mes]}")

            idx = int(input("\nEscolha o mês (1-12): ")) - 1
            if idx < 0 or idx >= len(meses):
                return

            mes = meses[idx]
            data = input("Data da atividade (ex: 15/03 ou '1º Domingo'): ").strip()
            descricao = input("Descrição da atividade: ").strip()

            if descricao:
                atividade = {"data": data, "descricao": descricao}
                if mes not in dados['atividades_planejadas_2024']:
                    dados['atividades_planejadas_2024'][mes] = []
                dados['atividades_planejadas_2024'][mes].append(atividade)
                print("✓ Atividade adicionada!")

        elif opcao == '2' or opcao == '3':
            # Editar ou remover
            print("\nMeses disponíveis:")
            for i, mes in enumerate(meses, 1):
                count = len(dados['atividades_planejadas_2024'].get(mes, []))
                print(f"{i}. {meses_nomes[mes]} ({count} atividades)")

            idx = int(input("\nEscolha o mês (1-12): ")) - 1
            if idx < 0 or idx >= len(meses):
                return

            mes = meses[idx]
            atividades = dados['atividades_planejadas_2024'].get(mes, [])

            if not atividades:
                print("Nenhuma atividade neste mês!")
                return

            print(f"\nAtividades de {meses_nomes[mes]}:")
            for i, ativ in enumerate(atividades, 1):
                data_str = f"{ativ['data']} – " if ativ.get('data') else ""
                print(f"{i}. {data_str}{ativ['descricao']}")

            ativ_idx = int(input("\nEscolha o número da atividade: ")) - 1
            if ativ_idx < 0 or ativ_idx >= len(atividades):
                return

            if opcao == '3':
                # Remover
                atividades.pop(ativ_idx)
                print("✓ Atividade removida!")
            else:
                # Editar
                ativ = atividades[ativ_idx]
                print(f"\nData atual: {ativ.get('data', '')}")
                nova_data = input("Nova data (Enter para manter): ").strip()
                if nova_data:
                    ativ['data'] = nova_data

                print(f"Descrição atual: {ativ['descricao']}")
                nova_desc = input("Nova descrição (Enter para manter): ").strip()
                if nova_desc:
                    ativ['descricao'] = nova_desc

                print("✓ Atividade atualizada!")

        elif opcao == '4':
            # Listar todas
            print("\n=== TODAS AS ATIVIDADES PLANEJADAS ===")
            for mes_key, mes_nome in meses_nomes.items():
                atividades = dados['atividades_planejadas_2024'].get(mes_key, [])
                if atividades:
                    print(f"\n{mes_nome}:")
                    for ativ in atividades:
                        data_str = f"{ativ['data']} – " if ativ.get('data') else ""
                        print(f"  • {data_str}{ativ['descricao']}")
            input("\nPressione Enter para continuar...")

    except (ValueError, KeyboardInterrupt):
        print("Operação cancelada.")


def editar_presidente_mensagem(dados):
    """Edita a mensagem da presidente"""
    print("\n=== EDITAR MENSAGEM DA PRESIDENTE ===")
    print(f"Nome atual: {dados['presidente']['nome']}")
    novo_nome = input("Novo nome (Enter para manter): ").strip()
    if novo_nome:
        dados['presidente']['nome'] = novo_nome

    print(f"\nMensagem atual:\n{dados['presidente']['mensagem']}")
    print(
        "\nDigite a nova mensagem (ou Enter para manter, 'editar' para editar linha por linha):"
    )
    nova_msg = input().strip()
    if nova_msg and nova_msg.lower() != 'editar':
        dados['presidente']['mensagem'] = nova_msg
        print("✓ Mensagem atualizada!")
    elif nova_msg.lower() == 'editar':
        print("Digite a nova mensagem (pressione Enter duas vezes para finalizar):")
        linhas = []
        while True:
            linha = input()
            if linha == "" and linhas and linhas[-1] == "":
                break
            linhas.append(linha)
        dados['presidente']['mensagem'] = "\n".join(linhas[:-1])
        print("✓ Mensagem atualizada!")


def editar_ano(dados):
    """Edita o ano da agenda"""
    print(f"\nAno atual: {dados['ano']}")
    novo_ano = input("Novo ano: ").strip()
    if novo_ano and novo_ano.isdigit():
        dados['ano'] = int(novo_ano)
        # Atualizar chave de atividades se necessário
        if f"atividades_planejadas_{dados['ano']}" not in dados:
            ano_antigo = dados['ano'] - 1
            if f"atividades_planejadas_{ano_antigo}" in dados:
                dados[f"atividades_planejadas_{dados['ano']}"] = dados.pop(
                    f"atividades_planejadas_{ano_antigo}"
                )
        print("✓ Ano atualizado!")
    else:
        print("Ano inválido!")


def editar_informacoes_gerais(dados):
    """Edita informações gerais"""
    print("\n=== EDITAR INFORMAÇÕES GERAIS ===")

    if 'informacoes_gerais' not in dados:
        dados['informacoes_gerais'] = {}

    info = dados['informacoes_gerais']

    # Missionário de oração
    if info.get('missionario_oracao'):
        miss = info['missionario_oracao']
        print(f"\n--- Missionário de Oração ---")
        print(f"Nome: {miss.get('nome', '')}")
        novo_nome = input("Novo nome (Enter para manter): ").strip()
        if novo_nome:
            miss['nome'] = novo_nome

        print(f"Data nascimento: {miss.get('data_nascimento', '')}")
        nova_data = input("Nova data (DD/MM, Enter para manter): ").strip()
        if nova_data:
            miss['data_nascimento'] = nova_data

        print(f"Campo: {miss.get('campo', '')}")
        novo_campo = input("Novo campo (Enter para manter): ").strip()
        if novo_campo:
            miss['campo'] = novo_campo

        print(f"WhatsApp: {miss.get('whatsapp', '')}")
        novo_whats = input("Novo WhatsApp (Enter para manter): ").strip()
        if novo_whats:
            miss['whatsapp'] = novo_whats

    # Observações
    if info.get('observacoes'):
        print(f"\n--- Observações ---")
        for i, obs in enumerate(info['observacoes'], 1):
            print(f"{i}. {obs}")
        print("0. Adicionar nova observação")

        escolha = input(
            "\nEscolha o número para editar/remover (0 para adicionar, Enter para pular): "
        ).strip()
        if escolha == '0':
            nova_obs = input("Nova observação: ").strip()
            if nova_obs:
                info['observacoes'].append(nova_obs)
                print("✓ Observação adicionada!")
        elif escolha.isdigit():
            idx = int(escolha) - 1
            if 0 <= idx < len(info['observacoes']):
                print(f"Observação atual: {info['observacoes'][idx]}")
                nova_obs = input(
                    "Nova observação (Enter para manter, 'remover' para remover): "
                ).strip()
                if nova_obs.lower() == 'remover':
                    info['observacoes'].pop(idx)
                    print("✓ Observação removida!")
                elif nova_obs:
                    info['observacoes'][idx] = nova_obs
                    print("✓ Observação atualizada!")

    print("✓ Informações gerais atualizadas!")


def menu_principal():
    """Menu principal"""
    dados = carregar_dados()
    if not dados:
        return

    while True:
        print("\n" + "=" * 50)
        print("EDITOR DE AGENDA - Federação de SAFs")
        print("=" * 50)
        print("1. Editar membro da diretoria")
        print("2. Editar SAF")
        print("3. Gerenciar atividades planejadas")
        print("4. Gerenciar atividades realizadas")
        print("5. Editar mensagem da presidente")
        print("6. Editar ano da agenda")
        print("7. Editar informações gerais")
        print("8. Visualizar dados (JSON)")
        print("9. Salvar e sair")
        print("0. Sair sem salvar")

        try:
            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == '1':
                editar_membro_diretoria(dados)
            elif opcao == '2':
                editar_saf(dados)
            elif opcao == '3':
                gerenciar_atividades(dados)
            elif opcao == '4':
                gerenciar_atividades_realizadas(dados)
            elif opcao == '5':
                editar_presidente_mensagem(dados)
            elif opcao == '6':
                editar_ano(dados)
            elif opcao == '7':
                editar_informacoes_gerais(dados)
            elif opcao == '8':
                print("\n" + json.dumps(dados, ensure_ascii=False, indent=2))
                input("\nPressione Enter para continuar...")
            elif opcao == '9':
                salvar_dados(dados)
                break
            elif opcao == '0':
                print("Alterações descartadas.")
                break
            else:
                print("Opção inválida!")

        except KeyboardInterrupt:
            print("\n\nOperação cancelada pelo usuário.")
            break
        except Exception as e:
            print(f"Erro: {e}")


if __name__ == "__main__":
    menu_principal()
