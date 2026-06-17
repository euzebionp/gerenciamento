@echo off
echo ===================================================
echo   Iniciando o Sistema de Gestao de Frota...
echo ===================================================

:: Verifica se o Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ O Python nao esta instalado nesta maquina.
    echo Por favor, instale o Python 3.8+ e marque a opcao "Add Python to PATH".
    pause
    exit
)

:: Define o diretorio atual como o diretorio do script
cd /d "%~dp0"

:: Cria o ambiente virtual se nao existir
if not exist "venv" (
    echo 📦 Criando ambiente virtual local (venv)...
    python -m venv venv
    call venv\Scripts\activate
    echo 📥 Instalando dependencias (isso pode levar alguns minutos na primeira execucao)...
    pip install -r requirements.txt
    echo 🗄️ Inicializando banco de dados...
    python seed.py
    python add_sample_data.py
) else (
    call venv\Scripts\activate
)

:: Executa o aplicativo Streamlit
echo 🚀 Abrindo o aplicativo no seu navegador...
streamlit run main.py --server.port=8501 --server.headless=false

pause
