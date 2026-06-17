import streamlit as st
import pandas as pd
from database import SessionLocal, Vehicle, VehicleStatus
from sqlalchemy.exc import IntegrityError

st.set_page_config(page_title="Veículos", page_icon="🚙", layout="wide")

if not st.session_state.get('authentication_status'):
    st.warning("Por favor, faça login na página principal.")
    st.stop()

st.title("🚙 Gestão de Veículos")

# Initialize session state for edit mode
if 'edit_vehicle_id' not in st.session_state:
    st.session_state.edit_vehicle_id = None
if 'delete_confirm_vehicle_id' not in st.session_state:
    st.session_state.delete_confirm_vehicle_id = None

tab1, tab2, tab3 = st.tabs(["Lista de Veículos", "Adicionar Novo", "Editar/Excluir"])

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
        
        st.info("💡 Use a aba 'Editar/Excluir' para modificar ou remover veículos.")
    else:
        st.info("Nenhum veículo cadastrado.")

with tab2:
    st.subheader("Novo Veículo")
    with st.form("new_vehicle"):
        plate = st.text_input("Placa (AAA-0000)").upper()
        model = st.text_input("Modelo (ex: Fiat Uno)")
        capacity = st.number_input("Capacidade", min_value=1, step=1, value=4)
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
                    st.success(f"✅ Veículo {model} ({plate}) cadastrado com sucesso!")
                    st.balloons()
                except IntegrityError:
                    db.rollback()
                    st.error("❌ Erro: Placa já cadastrada.")
                except Exception as e:
                    db.rollback()
                    st.error(f"❌ Erro ao salvar: {e}")

with tab3:
    st.subheader("Editar ou Excluir Veículo")
    
    vehicles = db.query(Vehicle).all()
    
    if not vehicles:
        st.warning("Nenhum veículo cadastrado para editar ou excluir.")
    else:
        # Select vehicle
        vehicle_options = {f"{v.model} - {v.plate}": v.id for v in vehicles}
        selected_vehicle_label = st.selectbox(
            "Selecione o veículo",
            options=list(vehicle_options.keys())
        )
        selected_vehicle_id = vehicle_options[selected_vehicle_label]
        selected_vehicle = db.query(Vehicle).filter(Vehicle.id == selected_vehicle_id).first()
        
        if selected_vehicle:
            st.markdown("---")
            
            # Edit and Delete columns
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### ✏️ Editar Veículo")
                
                with st.form("edit_vehicle"):
                    edit_plate = st.text_input("Placa", value=selected_vehicle.plate).upper()
                    edit_model = st.text_input("Modelo", value=selected_vehicle.model)
                    edit_capacity = st.number_input("Capacidade", min_value=1, step=1, value=selected_vehicle.capacity)
                    edit_type = st.selectbox(
                        "Tipo", 
                        ["Carro", "Van", "Ônibus", "Caminhão"],
                        index=["Carro", "Van", "Ônibus", "Caminhão"].index(selected_vehicle.type) if selected_vehicle.type in ["Carro", "Van", "Ônibus", "Caminhão"] else 0
                    )
                    edit_status = st.selectbox(
                        "Status",
                        [s.value for s in VehicleStatus],
                        index=[s.value for s in VehicleStatus].index(selected_vehicle.status.value)
                    )
                    
                    submit_edit = st.form_submit_button("💾 Salvar Alterações")
                    
                    if submit_edit:
                        if not edit_plate or not edit_model:
                            st.error("Preencha todos os campos obrigatórios!")
                        else:
                            try:
                                # Check if plate changed and is unique
                                if edit_plate != selected_vehicle.plate:
                                    existing = db.query(Vehicle).filter(Vehicle.plate == edit_plate).first()
                                    if existing:
                                        st.error("❌ Esta placa já está cadastrada em outro veículo!")
                                    else:
                                        selected_vehicle.plate = edit_plate
                                        selected_vehicle.model = edit_model
                                        selected_vehicle.capacity = edit_capacity
                                        selected_vehicle.type = edit_type
                                        selected_vehicle.status = VehicleStatus(edit_status)
                                        db.commit()
                                        st.success(f"✅ Veículo {edit_model} atualizado com sucesso!")
                                        st.rerun()
                                else:
                                    selected_vehicle.model = edit_model
                                    selected_vehicle.capacity = edit_capacity
                                    selected_vehicle.type = edit_type
                                    selected_vehicle.status = VehicleStatus(edit_status)
                                    db.commit()
                                    st.success(f"✅ Veículo {edit_model} atualizado com sucesso!")
                                    st.rerun()
                            except Exception as e:
                                db.rollback()
                                st.error(f"❌ Erro ao atualizar: {e}")
            
            with col2:
                st.markdown("### 🗑️ Excluir Veículo")
                st.warning(f"**Veículo:** {selected_vehicle.model}\n\n**Placa:** {selected_vehicle.plate}")
                
                # Check if vehicle has trips
                trip_count = len(selected_vehicle.trips) if hasattr(selected_vehicle, 'trips') else 0
                
                if trip_count > 0:
                    st.error(f"⚠️ Este veículo possui {trip_count} viagem(ns) registrada(s). Não é possível excluir.")
                else:
                    st.info("✓ Este veículo pode ser excluído.")
                    
                    # Confirmation checkbox
                    confirm_delete = st.checkbox("Confirmo que desejo excluir este veículo", key=f"confirm_delete_{selected_vehicle_id}")
                    
                    if st.button("🗑️ Excluir Veículo", type="primary", disabled=not confirm_delete):
                        try:
                            db.delete(selected_vehicle)
                            db.commit()
                            st.success(f"✅ Veículo {selected_vehicle.model} excluído com sucesso!")
                            st.session_state.edit_vehicle_id = None
                            st.balloons()
                            st.rerun()
                        except Exception as e:
                            db.rollback()
                            st.error(f"❌ Erro ao excluir: {e}")

db.close()
