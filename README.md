# 📚 Unimestre - Sistema de Gerenciamento Acadêmico

> Sistema simplificado para gerenciamento de alunos e aulas com integração ao Google Drive

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Google Drive](https://img.shields.io/badge/Storage-Google%20Drive-yellow.svg)](https://drive.google.com/)

## 🎯 Sobre o Projeto

**Unimestre** é um sistema de gerenciamento acadêmico desenvolvido em Python que permite professores cadastrarem alunos, registrarem notas com pesos, controlarem faltas e manterem um histórico de aulas. Todos os dados são armazenados de forma segura no Google Drive do usuário, sem ocupar espaço no computador local.

### ✨ Principais Funcionalidades

- 🔐 **Autenticação Google**: Login obrigatório com conta Google
- 👨‍🎓 **Gestão de Alunos**: Cadastro, listagem e atualização de informações
- 📊 **Sistema de Notas**: Notas com pesos personalizados e cálculo automático de média ponderada
- 📅 **Registro de Aulas**: Histórico completo de aulas ministradas
- ☁️ **Sincronização Automática**: Dados salvos automaticamente no Google Drive
- 🗑️ **Privacidade**: Arquivos locais são excluídos ao sair do sistema

## 🚀 Começando

### Pré-requisitos

- Python 3.8 ou superior
- Conta Google
- Projeto configurado no Google Cloud Console

### 📦 Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/unimestre.git
cd unimestre
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

### 🔑 Configuração do Google Drive API

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Ative a **Google Drive API**:
   - Vá em "APIs & Services" → "Enable APIs and Services"
   - Procure por "Google Drive API" e clique em "Enable"
4. Configure a tela de consentimento OAuth:
   - Vá em "OAuth consent screen"
   - Escolha "External" e preencha as informações básicas
   - Adicione seu email em "Test users"
5. Crie credenciais OAuth 2.0:
   - Vá em "Credentials" → "Create Credentials" → "OAuth client ID"
   - Escolha "Desktop app"
   - Baixe o arquivo JSON e renomeie para `client_secrets.json`
6. Coloque o arquivo `client_secrets.json` na raiz do projeto

### ▶️ Executando o Sistema

```bash
python main.py
```

Na primeira execução, o navegador abrirá automaticamente para você autorizar o acesso ao Google Drive.

## 📖 Como Usar

### Menu Principal

Após fazer login, você terá acesso às seguintes opções:

```
========== MENU PRINCIPAL ==========
1️⃣  Cadastrar aluno
2️⃣  Listar alunos
3️⃣  Atualizar aluno (faltas/notas)
4️⃣  Registrar aula
5️⃣  Listar aulas
6️⃣  Sair
===================================
```

### Cadastrar Aluno

- Informe o nome do aluno
- Defina o número inicial de faltas (geralmente 0)
- O aluno será salvo automaticamente no Google Drive

### Adicionar Notas

- Selecione a opção "Atualizar aluno"
- Escolha o aluno da lista
- Adicione notas com seus respectivos pesos
- A média ponderada é calculada automaticamente

### Critérios de Aprovação

- **Média mínima**: 7.0
- **Faltas máximas**: 5
- Ambos os critérios devem ser atendidos para aprovação

### Registrar Aulas

- Descreva o conteúdo da aula
- Data e hora são registradas automaticamente

## 🏗️ Estrutura do Projeto

```
unimestre/
├── main.py                 # Menu principal e fluxo do sistema
├── alunos.py              # Lógica de gerenciamento de alunos
├── aulas.py               # Lógica de registro de aulas
├── utils.py               # Funções auxiliares
├── drive_integration.py   # Integração com Google Drive
├── settings.yaml          # Configurações do PyDrive
├── client_secrets.json    # Credenciais OAuth (não versionado)
├── requirements.txt       # Dependências do projeto
└── README.md             # Este arquivo
```

## 🔒 Segurança e Privacidade

- ✅ Autenticação OAuth 2.0 com Google
- ✅ Dados armazenados apenas no Google Drive do usuário
- ✅ Arquivos locais temporários são excluídos ao sair
- ✅ Credenciais salvas localmente apenas para renovação de token
- ✅ Senha do professor para acesso ao sistema (padrão: `1234`)

> ⚠️ **Importante**: Altere a senha padrão no arquivo `main.py` (linha 30)

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **PyDrive**: Integração com Google Drive API
- **JSON**: Formato de armazenamento de dados
- **OAuth 2.0**: Autenticação segura

## 📝 Dependências

```
pydrive
PyYAML
```

## 🐛 Solução de Problemas

### Erro 403: access_denied

Se você receber este erro ao fazer login:

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Vá em "OAuth consent screen"
3. Adicione seu email em "Test users"
4. Delete o arquivo `credentials.json` e tente novamente

### Erro de Permissão no Windows

Se encontrar `PermissionError` ao salvar arquivos:

- O sistema já implementa retry automático
- Aguarde alguns segundos e tente novamente
- Certifique-se de que nenhum outro programa está acessando os arquivos

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abrir um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

Desenvolvido com ❤️ para facilitar a gestão acadêmica

## 📞 Suporte

Se você encontrar algum problema ou tiver sugestões, por favor:

- Abra uma [issue](https://github.com/seu-usuario/unimestre/issues)
- Entre em contato através do email: seu-email@exemplo.com

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub!
