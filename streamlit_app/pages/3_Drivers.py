import streamlit as st
import pandas as pd
from database import SessionLocal, Driver, DriverStatus
from sqlalchemy.exc import IntegrityError

st.set_page_config(page_title="Motoristas", page_icon="👨‍✈️", layout="wide")

if not st.session_state.get('authentication_status'):
    st.warning("Por favor, faça login na página principal.")
    st.stop()

st.title("👨‍✈️ Gestão de Motoristas")

tab1, tab2 = st.tabs(["Lista de Motoristas", "Adicionar Novo"])

db = SessionLocal()

with tab1:
    st.subheader("Motoristas Cadastrados")
    drivers = db.query(Driver).all()
    
    if drivers:
        data = [{
            "ID": d.id,
            "Nome": d.name,
            "CPF": d.cpf,
            "CNH": d.cnh,
            "Telefone": d.phone,
            "Status": d.status.value
        } for d in drivers]
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        # Edit/Delete section
        st.markdown("---")
        st.subheader("Editar Status do Motorista")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            driver_to_edit = st.selectbox(
                "Selecione o motorista",
                options=drivers,
                format_func=lambda d: f"{d.name} - {d.cpf}"
            )
        
        with col2:
            new_status = st.selectbox(
                "Novo Status",
                options=[s.value for s in DriverStatus],
                index=[s.value for s in DriverStatus].index(driver_to_edit.status.value) if driver_to_edit else 0
            )
        
        if st.button("Atualizar Status"):
            try:
                driver_to_edit.status = DriverStatus(new_status)
                db.commit()
                st.success(f"Status do motorista {driver_to_edit.name} atualizado com sucesso!")
                st.rerun()
            except Exception as e:
                db.rollback()
                st.error(f"Erro ao atualizar: {e}")
    else:
        st.info("Nenhum motorista cadastrado.")

with tab2:
    st.subheader("Novo Motorista")
    with st.form("new_driver"):
        name = st.text_input("Nome Completo")
        cpf = st.text_input("CPF (apenas números)")
        cnh = st.text_input("CNH (apenas números)")
        phone = st.text_input("Telefone (ex: 11999999999)")
        status = st.selectbox("Status", [s.value for s in DriverStatus])
        
        submit = st.form_submit_button("Salvar Motorista")
        
        if submit:
            if not name or not cpf or not cnh:
                st.error("Preencha todos os campos obrigatórios!")
            elif len(cpf) != 11 or not cpf.isdigit():
                st.error("CPF deve conter exatamente 11 dígitos numéricos!")
            elif len(cnh) < 9 or not cnh.isdigit():
                st.error("CNH deve conter pelo menos 9 dígitos numéricos!")
            else:
                try:
                    new_driver = Driver(
                        name=name,
                        cpf=cpf,
                        cnh=cnh,
                        phone=phone,
                        status=DriverStatus(status)
                    )
                    db.add(new_driver)
                    db.commit()
                    st.success(f"Motorista {name} cadastrado com sucesso!")
                    st.balloons()
                except IntegrityError:
                    db.rollback()
                    st.error("Erro: CPF ou CNH já cadastrados.")
                except Exception as e:
                    db.rollback()
                    st.error(f"Erro ao salvar: {e}")

db.close()
