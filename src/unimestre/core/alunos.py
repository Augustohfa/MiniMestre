from unimestre.shared.utils import salvar, carregar

ARQ_ALUNOS = "alunos.json"
# Carrega dados existentes
alunos = carregar(ARQ_ALUNOS)


def cadastrar_aluno():
    print("\n--- Cadastro de Aluno ---")
    nome = input("Nome do aluno: ").strip()
    faltas = int(input("Número de faltas iniciais (ou 0): "))

    print("✅ Aluno cadastrado com sucesso! (Notas serão adicionadas depois)")
    return {"nome": nome, "notas": [], "faltas": faltas}


def listar_alunos():
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return

    print("\n--- LISTA DE ALUNOS ---")
    for i, a in enumerate(alunos, start=1):
        if len(a['notas']) > 0:
            # Calcula média ponderada
            soma_notas = sum(nota['valor'] * nota['peso'] for nota in a['notas'])
            soma_pesos = sum(nota['peso'] for nota in a['notas'])
            media = soma_notas / soma_pesos if soma_pesos > 0 else 0
            situacao = "Aprovado" if media >= 7 and a['faltas'] <= 5 else "Reprovado"
            notas_str = ", ".join([f"{n['valor']} (peso {n['peso']})" for n in a['notas']])
            print(f"{i}. {a['nome']} - Notas: [{notas_str}] - Média: {media:.2f} - Faltas: {a['faltas']} - Situação: {situacao}")
        else:
            print(f"{i}. {a['nome']} - Sem notas ainda - Faltas: {a['faltas']} - Situação: Pendente")


def adicionar_aluno_e_salvar(aluno):
    alunos.append(aluno)
    salvar(ARQ_ALUNOS, alunos)


def atualizar_aluno():
    """Permite atualizar notas e faltas de um aluno já cadastrado"""
    if not alunos:
        print("⚠️ Nenhum aluno cadastrado ainda!")
        return

    listar_alunos()
    try:
        indice = int(input("\nDigite o número do aluno que deseja atualizar: ")) - 1
        if indice < 0 or indice >= len(alunos):
            print("❌ Aluno inválido.")
            return
    except ValueError:
        print("❌ Entrada inválida.")
        return

    aluno = alunos[indice]
    print(f"\nAtualizando: {aluno['nome']}")

    print("\nO que deseja alterar?")
    print("1 - Adicionar nova nota (com peso)")
    print("2 - Remover uma nota")
    print("3 - Atualizar número de faltas")
    print("4 - Ver detalhes das notas")
    opc = input("Escolha: ")

    if opc == "1":
        try:
            nova_nota = float(input("Digite a nova nota (0-10): "))
            if nova_nota < 0 or nova_nota > 10:
                print("❌ Nota deve estar entre 0 e 10.")
                return
            peso = float(input("Digite o peso da nota (ex: 1, 2, 3...): "))
            if peso <= 0:
                print("❌ Peso deve ser maior que 0.")
                return
            aluno["notas"].append({"valor": nova_nota, "peso": peso})
            print("✅ Nota adicionada com sucesso.")
        except ValueError:
            print("❌ Valor inválido.")
            return
    elif opc == "2":
        if not aluno["notas"]:
            print("⚠️ Não há notas para remover.")
            return
        print("\nNotas atuais:")
        for i, nota in enumerate(aluno["notas"], start=1):
            print(f"{i}. Nota: {nota['valor']} - Peso: {nota['peso']}")
        try:
            idx = int(input("Digite o número da nota a remover: ")) - 1
            if 0 <= idx < len(aluno["notas"]):
                removida = aluno["notas"].pop(idx)
                print(f"✅ Nota {removida['valor']} (peso {removida['peso']}) removida.")
            else:
                print("❌ Índice inválido.")
                return
        except ValueError:
            print("❌ Entrada inválida.")
            return
    elif opc == "3":
        try:
            aluno["faltas"] = int(input("Novo número de faltas: "))
            print("✅ Faltas atualizadas.")
        except ValueError:
            print("❌ Valor inválido.")
            return
    elif opc == "4":
        if not aluno["notas"]:
            print("⚠️ Nenhuma nota cadastrada ainda.")
            return
        print("\n--- Detalhes das Notas ---")
        for i, nota in enumerate(aluno["notas"], start=1):
            print(f"{i}. Nota: {nota['valor']} - Peso: {nota['peso']}")
        soma_notas = sum(nota['valor'] * nota['peso'] for nota in aluno['notas'])
        soma_pesos = sum(nota['peso'] for nota in aluno['notas'])
        media = soma_notas / soma_pesos if soma_pesos > 0 else 0
        print(f"\n📊 Média Ponderada: {media:.2f}")
        return
    else:
        print("⚠️ Opção inválida.")
        return

    salvar(ARQ_ALUNOS, alunos)
    print("💾 Alterações salvas com sucesso!")
