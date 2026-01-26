# 📦 Guia de Instalação

Este guia fornece instruções detalhadas para instalar e configurar o Sistema de Gestão de Frota.

## 📋 Requisitos do Sistema

### Obrigatórios
- **Python**: 3.8 ou superior
- **pip**: Gerenciador de pacotes Python
- **Sistema Operacional**: Windows, Linux ou macOS

### Recomendados
- **Git**: Para clonar o repositório
- **Ambiente Virtual**: Para isolar dependências

## 🚀 Instalação Rápida

### Windows

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/gestao-frota.git
cd gestao-frota/streamlit_app

# 2. Crie um ambiente virtual
python -m venv venv
venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicialize o banco de dados
python seed.py

# 5. (Opcional) Adicione dados de exemplo
python add_sample_data.py

# 6. Execute a aplicação
streamlit run main.py
```

### Linux/macOS

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/gestao-frota.git
cd gestao-frota/streamlit_app

# 2. Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicialize o banco de dados
python seed.py

# 5. (Opcional) Adicione dados de exemplo
python add_sample_data.py

# 6. Execute a aplicação
streamlit run main.py
```

## 📦 Dependências

O arquivo `requirements.txt` inclui:

```
streamlit>=1.31.0
sqlalchemy>=2.0.0
pandas>=2.0.0
bcrypt>=4.0.0
plotly>=5.18.0
watchdog>=3.0.0
```

### Instalação Individual

Se preferir instalar manualmente:

```bash
pip install streamlit sqlalchemy pandas bcrypt plotly watchdog
```

## 🗄️ Configuração do Banco de Dados

### Inicialização Automática

O script `seed.py` cria automaticamente:
- Banco de dados SQLite (`fleet.db`)
- Tabelas necessárias
- Usuário administrador padrão

```bash
python seed.py
```

**Credenciais criadas:**
- Usuário: `admin`
- Senha: `pmnp@123`

### Dados de Exemplo

Para facilitar testes, execute:

```bash
python add_sample_data.py
```

Isso adiciona:
- 5 veículos de diferentes tipos
- 5 motoristas com dados válidos
- 7 viagens em diferentes status

### Resetar Banco de Dados

Para limpar e recriar o banco:

```bash
# Windows
del fleet.db
python seed.py

# Linux/macOS
rm fleet.db
python seed.py
```

## 🔧 Configuração Avançada

### Porta Customizada

Para executar em uma porta diferente:

```bash
streamlit run main.py --server.port 8080
```

### Modo Headless

Para executar sem abrir o navegador:

```bash
streamlit run main.py --server.headless true
```

### Configuração Personalizada

Edite `.streamlit/config.toml` para customizar:
- Tema e cores
- Porta do servidor
- Configurações de segurança

## 🐳 Docker (Futuro)

Em breve será disponibilizada uma imagem Docker para facilitar o deployment.

## ⚠️ Solução de Problemas

### Erro: "No module named 'streamlit'"

**Solução:** Certifique-se de que o ambiente virtual está ativado e as dependências instaladas.

```bash
# Ative o ambiente virtual
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

pip install -r requirements.txt
```

### Erro: "Database is locked"

**Solução:** Feche todas as instâncias do Streamlit antes de executar scripts do banco.

```bash
# Pare o Streamlit (Ctrl+C no terminal)
# Execute o script desejado
python seed.py
```

### Erro: "Port 8501 is already in use"

**Solução:** Use uma porta diferente ou encerre o processo que está usando a porta.

```bash
# Use outra porta
streamlit run main.py --server.port 8502

# Ou encontre e encerre o processo
# Windows: netstat -ano | findstr :8501
# Linux: lsof -i :8501
```

### Erro de Importação do Plotly

**Solução:** Reinstale o Plotly.

```bash
pip uninstall plotly
pip install plotly
```

## 🔄 Atualização

Para atualizar para a versão mais recente:

```bash
# 1. Baixe as atualizações
git pull origin main

# 2. Atualize as dependências
pip install -r requirements.txt --upgrade

# 3. Execute migrações (se houver)
# (Instruções específicas serão fornecidas em cada release)
```

## 📞 Suporte

Se encontrar problemas durante a instalação:

1. Verifique a seção de [Issues](https://github.com/seu-usuario/gestao-frota/issues)
2. Abra uma nova issue com:
   - Sistema operacional
   - Versão do Python
   - Mensagem de erro completa
   - Passos para reproduzir

## ✅ Verificação da Instalação

Após a instalação, verifique se tudo está funcionando:

1. **Acesse:** http://localhost:8501
2. **Faça login** com as credenciais padrão
3. **Navegue** pelas páginas no menu lateral
4. **Teste** adicionar um veículo ou motorista

Se todas as etapas funcionarem, a instalação foi bem-sucedida! 🎉

---

**Próximo passo:** Leia o [README.md](README.md) para conhecer todas as funcionalidades.
