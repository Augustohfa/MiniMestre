# aulas.py - Registro e listagem de aulas

from utils import salvar, carregar
from datetime import datetime

ARQ_AULAS = "aulas.json"
aulas = carregar(ARQ_AULAS)


def registrar_aula():
    """Registra uma nova aula e salva no arquivo"""
    print("\n--- Registro de Aula ---")
    conteudo = input("Conteúdo da aula: ")
    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    aula = {"data": data, "conteudo": conteudo}
    aulas.append(aula)
    salvar(ARQ_AULAS, aulas)
    print("✅ Aula registrada com sucesso!")


def listar_aulas():
    """Lista todas as aulas já registradas"""
    if not aulas:
        print("Nenhuma aula registrada ainda.")
        return

    print("\n--- AULAS REGISTRADAS ---")
    for i, a in enumerate(aulas, start=1):
        print(f"{i}. {a['data']} - {a['conteudo']}")
