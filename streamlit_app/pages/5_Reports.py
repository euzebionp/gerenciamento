import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from database import SessionLocal, Trip, TripStatus, Vehicle, Driver, VehicleStatus
from sqlalchemy import func

st.set_page_config(page_title="Relatórios", page_icon="📊", layout="wide")

if not st.session_state.get('authentication_status'):
    st.warning("Por favor, faça login na página principal.")
    st.stop()

st.title("📊 Relatórios e Análises")

db = SessionLocal()

# Date range filter
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input(
        "Data Inicial",
        value=datetime.now() - timedelta(days=30)
    )
with col2:
    end_date = st.date_input(
        "Data Final",
        value=datetime.now()
    )

st.markdown("---")

# KPIs
st.subheader("📈 Indicadores Principais")

trips_in_period = db.query(Trip).filter(
    Trip.start_date >= datetime.combine(start_date, datetime.min.time()),
    Trip.start_date <= datetime.combine(end_date, datetime.max.time())
).all()

col1, col2, col3, col4 = st.columns(4)

total_trips = len(trips_in_period)
completed_trips = len([t for t in trips_in_period if t.status == TripStatus.CONCLUIDA])
total_distance = sum([t.distance_km for t in trips_in_period])
active_vehicles = db.query(Vehicle).filter(Vehicle.status == VehicleStatus.ATIVO).count()

col1.metric("Total de Viagens", total_trips)
col2.metric("Viagens Concluídas", completed_trips)
col3.metric("Distância Total (km)", f"{total_distance:,.1f}")
col4.metric("Veículos Ativos", active_vehicles)

st.markdown("---")

# Charts
tab1, tab2, tab3, tab4 = st.tabs(["Status das Viagens", "Por Veículo", "Por Motorista", "Tendências"])

with tab1:
    st.subheader("Distribuição por Status")
    
    if trips_in_period:
        status_counts = {}
        for trip in trips_in_period:
            status = trip.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        fig = px.pie(
            values=list(status_counts.values()),
            names=list(status_counts.keys()),
            title="Viagens por Status",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Status table
        st.dataframe(
            pd.DataFrame({
                "Status": list(status_counts.keys()),
                "Quantidade": list(status_counts.values())
            }),
            use_container_width=True
        )
    else:
        st.info("Nenhuma viagem no período selecionado.")

with tab2:
    st.subheader("Análise por Veículo")
    
    if trips_in_period:
        vehicle_stats = {}
        for trip in trips_in_period:
            vehicle_key = f"{trip.vehicle.model} ({trip.vehicle.plate})"
            if vehicle_key not in vehicle_stats:
                vehicle_stats[vehicle_key] = {
                    "trips": 0,
                    "distance": 0,
                    "completed": 0
                }
            vehicle_stats[vehicle_key]["trips"] += 1
            vehicle_stats[vehicle_key]["distance"] += trip.distance_km
            if trip.status == TripStatus.CONCLUIDA:
                vehicle_stats[vehicle_key]["completed"] += 1
        
        # Bar chart - trips per vehicle
        df_vehicles = pd.DataFrame([
            {
                "Veículo": k,
                "Viagens": v["trips"],
                "Distância (km)": v["distance"],
                "Concluídas": v["completed"]
            }
            for k, v in vehicle_stats.items()
        ])
        
        fig = px.bar(
            df_vehicles,
            x="Veículo",
            y="Viagens",
            title="Número de Viagens por Veículo",
            color="Concluídas",
            color_continuous_scale="Greens"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Distance chart
        fig2 = px.bar(
            df_vehicles,
            x="Veículo",
            y="Distância (km)",
            title="Distância Total por Veículo",
            color="Distância (km)",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        st.dataframe(df_vehicles, use_container_width=True)
    else:
        st.info("Nenhuma viagem no período selecionado.")

with tab3:
    st.subheader("Análise por Motorista")
    
    if trips_in_period:
        driver_stats = {}
        for trip in trips_in_period:
            driver_name = trip.driver.name
            if driver_name not in driver_stats:
                driver_stats[driver_name] = {
                    "trips": 0,
                    "distance": 0,
                    "completed": 0
                }
            driver_stats[driver_name]["trips"] += 1
            driver_stats[driver_name]["distance"] += trip.distance_km
            if trip.status == TripStatus.CONCLUIDA:
                driver_stats[driver_name]["completed"] += 1
        
        df_drivers = pd.DataFrame([
            {
                "Motorista": k,
                "Viagens": v["trips"],
                "Distância (km)": v["distance"],
                "Concluídas": v["completed"],
                "Taxa de Conclusão (%)": round((v["completed"] / v["trips"]) * 100, 1) if v["trips"] > 0 else 0
            }
            for k, v in driver_stats.items()
        ])
        
        # Horizontal bar chart
        fig = px.bar(
            df_drivers.sort_values("Viagens", ascending=True),
            y="Motorista",
            x="Viagens",
            orientation='h',
            title="Viagens por Motorista",
            color="Taxa de Conclusão (%)",
            color_continuous_scale="RdYlGn"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df_drivers, use_container_width=True)
    else:
        st.info("Nenhuma viagem no período selecionado.")

with tab4:
    st.subheader("Tendências ao Longo do Tempo")
    
    if trips_in_period:
        # Group by date
        daily_stats = {}
        for trip in trips_in_period:
            date_key = trip.start_date.date()
            if date_key not in daily_stats:
                daily_stats[date_key] = {
                    "trips": 0,
                    "distance": 0
                }
            daily_stats[date_key]["trips"] += 1
            daily_stats[date_key]["distance"] += trip.distance_km
        
        df_daily = pd.DataFrame([
            {
                "Data": k,
                "Viagens": v["trips"],
                "Distância (km)": v["distance"]
            }
            for k, v in sorted(daily_stats.items())
        ])
        
        # Line chart - trips over time
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_daily["Data"],
            y=df_daily["Viagens"],
            mode='lines+markers',
            name='Viagens',
            line=dict(color='#1f77b4', width=2)
        ))
        fig.update_layout(
            title="Viagens ao Longo do Tempo",
            xaxis_title="Data",
            yaxis_title="Número de Viagens",
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Line chart - distance over time
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df_daily["Data"],
            y=df_daily["Distância (km)"],
            mode='lines+markers',
            name='Distância',
            line=dict(color='#ff7f0e', width=2),
            fill='tozeroy'
        ))
        fig2.update_layout(
            title="Distância Percorrida ao Longo do Tempo",
            xaxis_title="Data",
            yaxis_title="Distância (km)",
            hovermode='x unified'
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        st.dataframe(df_daily, use_container_width=True)
    else:
        st.info("Nenhuma viagem no período selecionado.")

# Export section
st.markdown("---")
st.subheader("📥 Exportar Dados")

if trips_in_period:
    export_data = [{
        "ID": t.id,
        "Origem": t.origin,
        "Destino": t.destination,
        "Veículo": f"{t.vehicle.model} ({t.vehicle.plate})",
        "Motorista": t.driver.name,
        "Data Início": t.start_date.strftime('%d/%m/%Y %H:%M'),
        "Data Fim": t.end_date.strftime('%d/%m/%Y %H:%M') if t.end_date else "N/A",
        "Distância (km)": t.distance_km,
        "Status": t.status.value
    } for t in trips_in_period]
    
    df_export = pd.DataFrame(export_data)
    csv = df_export.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Baixar Relatório Completo (CSV)",
        data=csv,
        file_name=f"relatorio_viagens_{start_date}_{end_date}.csv",
        mime="text/csv"
    )
else:
    st.info("Nenhum dado disponível para exportação no período selecionado.")

db.close()
