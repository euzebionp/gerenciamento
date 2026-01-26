import streamlit as st
import pandas as pd
from database import SessionLocal, Driver, DriverStatus
from sqlalchemy.exc import IntegrityError

st.set_page_config(page_title="Motoristas", page_icon="👨‍✈️", layout="wide")

if not st.session_state.get('authentication_status'):
    st.warning("Por favor, faça login na página principal.")
    st.stop()

st.title("👨‍✈️ Gestão de Motoristas")

tab1, tab2, tab3 = st.tabs(["Lista de Motoristas", "Adicionar Novo", "Editar/Excluir"])

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
        
        st.info("💡 Use a aba 'Editar/Excluir' para modificar ou remover motoristas.")
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
                    st.success(f"✅ Motorista {name} cadastrado com sucesso!")
                    st.balloons()
                except IntegrityError:
                    db.rollback()
                    st.error("❌ Erro: CPF ou CNH já cadastrados.")
                except Exception as e:
                    db.rollback()
                    st.error(f"❌ Erro ao salvar: {e}")

with tab3:
    st.subheader("Editar ou Excluir Motorista")
    
    drivers = db.query(Driver).all()
    
    if not drivers:
        st.warning("Nenhum motorista cadastrado para editar ou excluir.")
    else:
        # Select driver
        driver_options = {f"{d.name} - CPF: {d.cpf}": d.id for d in drivers}
        selected_driver_label = st.selectbox(
            "Selecione o motorista",
            options=list(driver_options.keys())
        )
        selected_driver_id = driver_options[selected_driver_label]
        selected_driver = db.query(Driver).filter(Driver.id == selected_driver_id).first()
        
        if selected_driver:
            st.markdown("---")
            
            # Edit and Delete columns
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### ✏️ Editar Motorista")
                
                with st.form("edit_driver"):
                    edit_name = st.text_input("Nome Completo", value=selected_driver.name)
                    edit_cpf = st.text_input("CPF", value=selected_driver.cpf)
                    edit_cnh = st.text_input("CNH", value=selected_driver.cnh)
                    edit_phone = st.text_input("Telefone", value=selected_driver.phone or "")
                    edit_status = st.selectbox(
                        "Status",
                        [s.value for s in DriverStatus],
                        index=[s.value for s in DriverStatus].index(selected_driver.status.value)
                    )
                    
                    submit_edit = st.form_submit_button("💾 Salvar Alterações")
                    
                    if submit_edit:
                        if not edit_name or not edit_cpf or not edit_cnh:
                            st.error("Preencha todos os campos obrigatórios!")
                        elif len(edit_cpf) != 11 or not edit_cpf.isdigit():
                            st.error("CPF deve conter exatamente 11 dígitos numéricos!")
                        elif len(edit_cnh) < 9 or not edit_cnh.isdigit():
                            st.error("CNH deve conter pelo menos 9 dígitos numéricos!")
                        else:
                            try:
                                # Check if CPF changed and is unique
                                if edit_cpf != selected_driver.cpf:
                                    existing = db.query(Driver).filter(Driver.cpf == edit_cpf).first()
                                    if existing:
                                        st.error("❌ Este CPF já está cadastrado em outro motorista!")
                                    else:
                                        # Check CNH uniqueness
                                        if edit_cnh != selected_driver.cnh:
                                            existing_cnh = db.query(Driver).filter(Driver.cnh == edit_cnh).first()
                                            if existing_cnh:
                                                st.error("❌ Esta CNH já está cadastrada em outro motorista!")
                                            else:
                                                selected_driver.name = edit_name
                                                selected_driver.cpf = edit_cpf
                                                selected_driver.cnh = edit_cnh
                                                selected_driver.phone = edit_phone
                                                selected_driver.status = DriverStatus(edit_status)
                                                db.commit()
                                                st.success(f"✅ Motorista {edit_name} atualizado com sucesso!")
                                                st.rerun()
                                        else:
                                            selected_driver.name = edit_name
                                            selected_driver.cpf = edit_cpf
                                            selected_driver.phone = edit_phone
                                            selected_driver.status = DriverStatus(edit_status)
                                            db.commit()
                                            st.success(f"✅ Motorista {edit_name} atualizado com sucesso!")
                                            st.rerun()
                                else:
                                    # CPF didn't change, check CNH
                                    if edit_cnh != selected_driver.cnh:
                                        existing_cnh = db.query(Driver).filter(Driver.cnh == edit_cnh).first()
                                        if existing_cnh:
                                            st.error("❌ Esta CNH já está cadastrada em outro motorista!")
                                        else:
                                            selected_driver.name = edit_name
                                            selected_driver.cnh = edit_cnh
                                            selected_driver.phone = edit_phone
                                            selected_driver.status = DriverStatus(edit_status)
                                            db.commit()
                                            st.success(f"✅ Motorista {edit_name} atualizado com sucesso!")
                                            st.rerun()
                                    else:
                                        selected_driver.name = edit_name
                                        selected_driver.phone = edit_phone
                                        selected_driver.status = DriverStatus(edit_status)
                                        db.commit()
                                        st.success(f"✅ Motorista {edit_name} atualizado com sucesso!")
                                        st.rerun()
                            except Exception as e:
                                db.rollback()
                                st.error(f"❌ Erro ao atualizar: {e}")
            
            with col2:
                st.markdown("### 🗑️ Excluir Motorista")
                st.warning(f"**Nome:** {selected_driver.name}\n\n**CPF:** {selected_driver.cpf}\n\n**CNH:** {selected_driver.cnh}")
                
                # Check if driver has trips
                trip_count = len(selected_driver.trips) if hasattr(selected_driver, 'trips') else 0
                
                if trip_count > 0:
                    st.error(f"⚠️ Este motorista possui {trip_count} viagem(ns) registrada(s). Não é possível excluir.")
                else:
                    st.info("✓ Este motorista pode ser excluído.")
                    
                    # Confirmation checkbox
                    confirm_delete = st.checkbox("Confirmo que desejo excluir este motorista", key=f"confirm_delete_driver_{selected_driver_id}")
                    
                    if st.button("🗑️ Excluir Motorista", type="primary", disabled=not confirm_delete):
                        try:
                            db.delete(selected_driver)
                            db.commit()
                            st.success(f"✅ Motorista {selected_driver.name} excluído com sucesso!")
                            st.balloons()
                            st.rerun()
                        except Exception as e:
                            db.rollback()
                            st.error(f"❌ Erro ao excluir: {e}")

db.close()
