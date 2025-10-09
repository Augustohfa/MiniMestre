# Funções auxiliares de leitura e escrita de JSON
# Integradas ao Google Drive via camada infra

from unimestre.infra.drive import carregar_json_do_drive, salvar_json_no_drive


def carregar(arquivo):
    """Carrega dados de um arquivo JSON do Google Drive"""
    return carregar_json_do_drive(arquivo)


def salvar(arquivo, dados):
    """Salva dados (lista ou dicionário) em um arquivo JSON no Google Drive"""
    salvar_json_no_drive(arquivo, dados)
