import streamlit as st
import pandas as pd
from datetime import datetime, date
from database import SessionLocal, Trip, TripStatus, Vehicle, Driver
from sqlalchemy.exc import IntegrityError

st.set_page_config(page_title="Viagens", page_icon="🗺️", layout="wide")

if not st.session_state.get('authentication_status'):
    st.warning("Por favor, faça login na página principal.")
    st.stop()

st.title("🗺️ Gestão de Viagens")

tab1, tab2, tab3 = st.tabs(["Viagens Ativas", "Histórico", "Nova Viagem"])

db = SessionLocal()

with tab1:
    st.subheader("Viagens em Andamento")
    active_trips = db.query(Trip).filter(
        Trip.status.in_([TripStatus.PLANEJADA, TripStatus.EM_ANDAMENTO])
    ).all()
    
    if active_trips:
        for trip in active_trips:
            with st.expander(f"🚗 Viagem #{trip.id} - {trip.origin} → {trip.destination}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Veículo:** {trip.vehicle.model} ({trip.vehicle.plate})")
                    st.write(f"**Motorista:** {trip.driver.name}")
                
                with col2:
                    st.write(f"**Data Início:** {trip.start_date.strftime('%d/%m/%Y %H:%M')}")
                    if trip.end_date:
                        st.write(f"**Data Fim:** {trip.end_date.strftime('%d/%m/%Y %H:%M')}")
                    else:
                        st.write(f"**Data Fim:** Não finalizada")
                
                with col3:
                    st.write(f"**Distância:** {trip.distance_km} km")
                    st.write(f"**Status:** {trip.status.value}")
                
                # Status update
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    new_status = st.selectbox(
                        "Atualizar Status",
                        options=[s.value for s in TripStatus],
                        key=f"status_{trip.id}",
                        index=[s.value for s in TripStatus].index(trip.status.value)
                    )
                
                with col_b:
                    if st.button("Atualizar", key=f"btn_{trip.id}"):
                        try:
                            trip.status = TripStatus(new_status)
                            if new_status == TripStatus.CONCLUIDA.value and not trip.end_date:
                                trip.end_date = datetime.now()
                            db.commit()
                            st.success("Status atualizado!")
                            st.rerun()
                        except Exception as e:
                            db.rollback()
                            st.error(f"Erro: {e}")
    else:
        st.info("Nenhuma viagem ativa no momento.")

with tab2:
    st.subheader("Histórico de Viagens")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        filter_status = st.multiselect(
            "Filtrar por Status",
            options=[s.value for s in TripStatus],
            default=[TripStatus.CONCLUIDA.value]
        )
    
    with col2:
        filter_date = st.date_input("Filtrar por Data (a partir de)", value=None)
    
    # Query with filters
    query = db.query(Trip)
    
    if filter_status:
        query = query.filter(Trip.status.in_([TripStatus(s) for s in filter_status]))
    
    if filter_date:
        query = query.filter(Trip.start_date >= datetime.combine(filter_date, datetime.min.time()))
    
    trips = query.order_by(Trip.start_date.desc()).all()
    
    if trips:
        data = [{
            "ID": t.id,
            "Origem": t.origin,
            "Destino": t.destination,
            "Veículo": f"{t.vehicle.model} ({t.vehicle.plate})",
            "Motorista": t.driver.name,
            "Data Início": t.start_date.strftime('%d/%m/%Y %H:%M'),
            "Data Fim": t.end_date.strftime('%d/%m/%Y %H:%M') if t.end_date else "N/A",
            "Distância (km)": t.distance_km,
            "Status": t.status.value
        } for t in trips]
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        # Export option
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Exportar para CSV",
            data=csv,
            file_name=f"viagens_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("Nenhuma viagem encontrada com os filtros selecionados.")

with tab3:
    st.subheader("Registrar Nova Viagem")
    
    # Get available vehicles and drivers
    vehicles = db.query(Vehicle).filter(Vehicle.status == "ATIVO").all()
    drivers = db.query(Driver).filter(Driver.status == "ATIVO").all()
    
    if not vehicles:
        st.warning("⚠️ Nenhum veículo ativo disponível. Cadastre veículos primeiro.")
    elif not drivers:
        st.warning("⚠️ Nenhum motorista ativo disponível. Cadastre motoristas primeiro.")
    else:
        with st.form("new_trip"):
            col1, col2 = st.columns(2)
            
            with col1:
                origin = st.text_input("Origem")
                destination = st.text_input("Destino")
                distance_km = st.number_input("Distância (km)", min_value=0.0, step=0.1)
            
            with col2:
                vehicle = st.selectbox(
                    "Veículo",
                    options=vehicles,
                    format_func=lambda v: f"{v.model} ({v.plate})"
                )
                driver = st.selectbox(
                    "Motorista",
                    options=drivers,
                    format_func=lambda d: f"{d.name} - CNH: {d.cnh}"
                )
                start_date = st.date_input("Data de Início", value=date.today())
                start_time = st.time_input("Hora de Início")
            
            status = st.selectbox("Status Inicial", [TripStatus.PLANEJADA.value, TripStatus.EM_ANDAMENTO.value])
            
            submit = st.form_submit_button("Registrar Viagem")
            
            if submit:
                if not origin or not destination:
                    st.error("Preencha origem e destino!")
                elif distance_km <= 0:
                    st.error("A distância deve ser maior que zero!")
                else:
                    try:
                        start_datetime = datetime.combine(start_date, start_time)
                        
                        new_trip = Trip(
                            origin=origin,
                            destination=destination,
                            distance_km=distance_km,
                            start_date=start_datetime,
                            vehicle_id=vehicle.id,
                            driver_id=driver.id,
                            status=TripStatus(status)
                        )
                        db.add(new_trip)
                        db.commit()
                        st.success(f"✅ Viagem de {origin} para {destination} registrada com sucesso!")
                        st.balloons()
                    except Exception as e:
                        db.rollback()
                        st.error(f"Erro ao registrar viagem: {e}")

db.close()
