from alunos import (
    cadastrar_aluno,
    listar_alunos,
    adicionar_aluno_e_salvar,
    atualizar_aluno
)
from aulas import registrar_aula, listar_aulas
from drive_integration import inicializar_drive, limpar_arquivos_locais


def menu():
    print("📚 Bem-vindo ao sistema UNIMESTRE SIMPLIFICADO!")
    
    # Login obrigatório com Google Drive
    print("\n" + "="*50)
    print("🔐 AUTENTICAÇÃO NECESSÁRIA")
    print("="*50)
    print("Este sistema armazena os dados no seu Google Drive.")
    print("Você será redirecionado para fazer login com sua conta Google.")
    print("="*50 + "\n")
    
    try:
        inicializar_drive()
    except Exception as e:
        print(f"\n❌ Erro ao conectar com Google Drive: {e}")
        print("O sistema não pode continuar sem autenticação.")
        return

    # Senha do professor
    senha_professor = "1234"
    if input("\nDigite a senha do professor: ") != senha_professor:
        print("Senha incorreta. Saindo...")
        return

    while True:
        print("\n========== MENU PRINCIPAL ==========")
        print("1️⃣  Cadastrar aluno")
        print("2️⃣  Listar alunos")
        print("3️⃣  Atualizar aluno (faltas/notas)")
        print("4️⃣  Registrar aula")
        print("5️⃣  Listar aulas")
        print("6️⃣  Sair")
        print("===================================")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            aluno = cadastrar_aluno()
            adicionar_aluno_e_salvar(aluno)
        elif opcao == "2":
            listar_alunos()
        elif opcao == "3":
            atualizar_aluno()
        elif opcao == "4":
            registrar_aula()
        elif opcao == "5":
            listar_aulas()
        elif opcao == "6":
            print("\n👋 Saindo do sistema...")
            print("🧹 Limpando arquivos locais...")
            limpar_arquivos_locais()
            print("✅ Sistema encerrado. Seus dados estão seguros no Google Drive!")
            break
        else:
            print("⚠️ Opção inválida! Tente novamente.")


if __name__ == '__main__':
    menu()