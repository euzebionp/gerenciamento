import streamlit as st
from database import SessionLocal, Vehicle, Driver, Trip, TripStatus

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

if not st.session_state.get('authentication_status'):
    st.warning("Por favor, faça login na página principal.")
    st.stop()

st.title("📊 Dashboard")

db = SessionLocal()

# Metrics
col1, col2, col3, col4 = st.columns(4)

total_vehicles = db.query(Vehicle).count()
active_vehicles = db.query(Vehicle).filter(Vehicle.status == "ATIVO").count()
total_drivers = db.query(Driver).count()
active_trips = db.query(Trip).filter(Trip.status == TripStatus.EM_ANDAMENTO).count()

col1.metric("Veículos Totais", total_vehicles)
col2.metric("Veículos Ativos", active_vehicles)
col3.metric("Motoristas", total_drivers)
col4.metric("Viagens em Andamento", active_trips)

st.markdown("---")

# Recent Activity (Placeholder or fetch logs if implemented)
st.subheader("Atividade Recente")
st.info("Funcionalidade de logs será implementada em breve.")

db.close()
