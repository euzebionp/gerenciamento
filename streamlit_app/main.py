import streamlit as st
import time
from database import SessionLocal, User
from auth import verify_password

st.set_page_config(page_title="Gestão de Frota", page_icon="🚗", layout="wide")

# Session State Initialization
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'role' not in st.session_state:
    st.session_state['role'] = None

def login():
    st.title("🔐 Login - Gestão de Frota")
    
    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")
        
        if submit:
            db = SessionLocal()
            user = db.query(User).filter(User.username == username).first()
            db.close()
            
            if user and verify_password(user.password, password):
                st.session_state['authentication_status'] = True
                st.session_state['username'] = user.username
                st.session_state['role'] = user.role.value
                st.success(f"Bem-vindo, {user.username}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")

def logout():
    st.session_state['authentication_status'] = None
    st.session_state['username'] = None
    st.session_state['role'] = None
    st.rerun()

# Main Logic
if st.session_state['authentication_status']:
    st.sidebar.title(f"👤 {st.session_state['username']}")
    st.sidebar.write(f"Perfil: {st.session_state['role']}")
    
    if st.sidebar.button("Sair"):
        logout()
    
    st.write("# Bem-vindo ao Sistema de Gestão de Frota")
    st.write("Use o menu lateral para navegar entre as funcionalidades.")
    
    st.info("👈 Selecione uma página no menu lateral para começar.")
    
else:
    login()
