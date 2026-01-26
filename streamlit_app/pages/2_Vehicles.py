import streamlit as st
import pandas as pd
from database import SessionLocal, Vehicle, VehicleStatus
from sqlalchemy.exc import IntegrityError

st.set_page_config(page_title="Veículos", page_icon="🚙", layout="wide")

if not st.session_state.get('authentication_status'):
    st.warning("Por favor, faça login na página principal.")
    st.stop()

st.title("🚙 Gestão de Veículos")

tab1, tab2 = st.tabs(["Lista de Veículos", "Adicionar Novo"])

db = SessionLocal()

with tab1:
    st.subheader("Veículos Cadastrados")
    vehicles = db.query(Vehicle).all()
    
    if vehicles:
        data = [{
            "ID": v.id,
            "Placa": v.plate,
            "Modelo": v.model,
            "Capacidade": v.capacity,
            "Tipo": v.type,
            "Status": v.status.value
        } for v in vehicles]
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        # Edit/Delete Placeholder (Streamlit needs a bit more logic for row actions, kept simple for now)
        st.caption("Para editar ou remover, entre em contato com o suporte ou use a admin.")
    else:
        st.info("Nenhum veículo cadastrado.")

with tab2:
    st.subheader("Novo Veículo")
    with st.form("new_vehicle"):
        plate = st.text_input("Placa (AAA-0000)").upper()
        model = st.text_input("Modelo (ex: Fiat Uno)")
        capacity = st.number_input("Capacidade", min_value=1, step=1)
        v_type = st.selectbox("Tipo", ["Carro", "Van", "Ônibus", "Caminhão"])
        status = st.selectbox("Status", [s.value for s in VehicleStatus])
        
        submit = st.form_submit_button("Salvar Veículo")
        
        if submit:
            if not plate or not model:
                st.error("Preencha todos os campos obrigatórios!")
            else:
                try:
                    new_vehicle = Vehicle(
                        plate=plate,
                        model=model,
                        capacity=capacity,
                        type=v_type,
                        status=VehicleStatus(status)
                    )
                    db.add(new_vehicle)
                    db.commit()
                    st.success(f"Veículo {model} ({plate}) cadastrado com sucesso!")
                except IntegrityError:
                    db.rollback()
                    st.error("Erro: Placa já cadastrada.")
                except Exception as e:
                    db.rollback()
                    st.error(f"Erro ao salvar: {e}")

db.close()
