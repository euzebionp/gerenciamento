import os
import sys
import streamlit.web.cli as stcli

if __name__ == '__main__':
    # Obtém o caminho absoluto do diretório onde o executável/script está rodando
    if getattr(sys, 'frozen', False):
        # Se estiver rodando como executável compilado pelo PyInstaller
        base_dir = sys._MEIPASS
    else:
        # Se estiver rodando como script Python comum
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    main_py_path = os.path.join(base_dir, "main.py")
    
    # Define os argumentos para executar o streamlit
    sys.argv = [
        "streamlit",
        "run",
        main_py_path,
        "--global.developmentMode=false",
        "--server.port=8501",
        "--server.headless=true"
    ]
    
    sys.exit(stcli.main())
