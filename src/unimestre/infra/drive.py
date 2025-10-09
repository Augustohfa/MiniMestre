from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import json
import os
import time

_drive = None
_gauth = None


def inicializar_drive():
    """Inicializa e autentica com Google Drive"""
    global _drive, _gauth
    if _drive is not None:
        return _drive

    print("\n🔐 Iniciando autenticação com Google Drive...")
    _gauth = GoogleAuth()

    # Tenta carregar credenciais salvas
    _gauth.LoadCredentialsFile("credentials.json")

    if _gauth.credentials is None:
        # Primeira autenticação
        try:
            _gauth.LocalWebserverAuth()
        except:
            _gauth.CommandLineAuth()
    elif _gauth.access_token_expired:
        # Renova token expirado
        _gauth.Refresh()
    else:
        # Usa credenciais salvas
        _gauth.Authorize()

    # Salva credenciais para próxima vez
    _gauth.SaveCredentialsFile("credentials.json")

    _drive = GoogleDrive(_gauth)
    print("✅ Autenticação realizada com sucesso!")
    return _drive


def buscar_arquivo_no_drive(nome_arquivo):
    """Busca um arquivo no Drive pelo nome"""
    drive = inicializar_drive()
    query = f"title='{nome_arquivo}' and trashed=false"
    arquivos = drive.ListFile({'q': query}).GetList()
    return arquivos[0] if arquivos else None


def carregar_json_do_drive(nome_arquivo):
    """Carrega dados JSON diretamente do Drive sem criar arquivo local permanente"""
    drive = inicializar_drive()
    arquivo = buscar_arquivo_no_drive(nome_arquivo)

    if not arquivo:
        print(f"📄 {nome_arquivo} não encontrado no Drive. Criando novo...")
        return []

    # Baixa temporariamente para ler
    temp_file = f"_temp_{nome_arquivo}"
    try:
        arquivo.GetContentFile(temp_file)
        with open(temp_file, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        print(f"⬇️ {nome_arquivo} carregado do Drive")
        return dados
    except Exception as e:
        print(f"⚠️ Erro ao carregar {nome_arquivo}: {e}")
        return []
    finally:
        # Remove arquivo temporário com retry para Windows
        _remover_arquivo_seguro(temp_file)


def salvar_json_no_drive(nome_arquivo, dados):
    """Salva dados JSON diretamente no Drive"""
    drive = inicializar_drive()

    # Cria arquivo temporário local
    temp_file = f"_temp_{nome_arquivo}"
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    # Garante que o arquivo foi fechado
    time.sleep(0.1)

    try:
        arquivo = buscar_arquivo_no_drive(nome_arquivo)

        if arquivo:
            # Atualiza arquivo existente
            arquivo.SetContentFile(temp_file)
            arquivo.Upload()
        else:
            # Cria novo arquivo
            arquivo = drive.CreateFile({'title': nome_arquivo})
            arquivo.SetContentFile(temp_file)
            arquivo.Upload()

        print(f"☁️ {nome_arquivo} salvo no Drive")
    finally:
        # Remove arquivo temporário com retry para Windows
        _remover_arquivo_seguro(temp_file)


def _remover_arquivo_seguro(caminho_arquivo):
    """Remove arquivo com retry para evitar erro de permissão no Windows"""
    if not os.path.exists(caminho_arquivo):
        return

    max_tentativas = 5
    for tentativa in range(max_tentativas):
        try:
            os.remove(caminho_arquivo)
            return
        except PermissionError:
            if tentativa < max_tentativas - 1:
                time.sleep(0.2)  # Aguarda 200ms antes de tentar novamente
            else:
                # Se falhar após todas as tentativas, apenas avisa
                print(f"⚠️ Não foi possível remover {caminho_arquivo} (arquivo em uso)")


def limpar_arquivos_locais():
    """Remove arquivos JSON locais ao fechar o aplicativo"""
    arquivos = ["alunos.json", "aulas.json"]
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            _remover_arquivo_seguro(arquivo)
            if not os.path.exists(arquivo):
                print(f"🗑️ {arquivo} removido do computador")

    # Remove também arquivos temporários que possam ter ficado
    try:
        for arquivo in os.listdir('.'):
            if arquivo.startswith('_temp_') and arquivo.endswith('.json'):
                _remover_arquivo_seguro(arquivo)
                if not os.path.exists(arquivo):
                    print(f"🗑️ {arquivo} (temporário) removido")
    except Exception:
        pass
