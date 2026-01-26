from database import SessionLocal, Vehicle, Driver, Trip, VehicleStatus, DriverStatus, TripStatus
from datetime import datetime, timedelta

def add_sample_data():
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Vehicle).count() > 0:
            print("Sample data already exists. Skipping...")
            return
        
        print("Adding sample vehicles...")
        vehicles = [
            Vehicle(plate="ABC-1234", model="Fiat Uno", capacity=4, type="Carro", status=VehicleStatus.ATIVO),
            Vehicle(plate="DEF-5678", model="Volkswagen Kombi", capacity=8, type="Van", status=VehicleStatus.ATIVO),
            Vehicle(plate="GHI-9012", model="Mercedes-Benz Sprinter", capacity=15, type="Van", status=VehicleStatus.ATIVO),
            Vehicle(plate="JKL-3456", model="Iveco Daily", capacity=20, type="Ônibus", status=VehicleStatus.ATIVO),
            Vehicle(plate="MNO-7890", model="Ford Cargo", capacity=2, type="Caminhão", status=VehicleStatus.MANUTENCAO),
        ]
        db.add_all(vehicles)
        db.commit()
        print(f"✓ Added {len(vehicles)} vehicles")
        
        print("Adding sample drivers...")
        drivers = [
            Driver(name="João Silva", cpf="12345678901", cnh="123456789", phone="11987654321", status=DriverStatus.ATIVO),
            Driver(name="Maria Santos", cpf="98765432109", cnh="987654321", phone="11912345678", status=DriverStatus.ATIVO),
            Driver(name="Pedro Oliveira", cpf="45678912301", cnh="456789123", phone="11923456789", status=DriverStatus.ATIVO),
            Driver(name="Ana Costa", cpf="78912345601", cnh="789123456", phone="11934567890", status=DriverStatus.FERIAS),
            Driver(name="Carlos Souza", cpf="32165498701", cnh="321654987", phone="11945678901", status=DriverStatus.ATIVO),
        ]
        db.add_all(drivers)
        db.commit()
        print(f"✓ Added {len(drivers)} drivers")
        
        print("Adding sample trips...")
        trips = [
            Trip(
                origin="São Paulo - SP",
                destination="Rio de Janeiro - RJ",
                distance_km=430.5,
                start_date=datetime.now() - timedelta(days=5),
                end_date=datetime.now() - timedelta(days=4),
                vehicle_id=vehicles[0].id,
                driver_id=drivers[0].id,
                status=TripStatus.CONCLUIDA
            ),
            Trip(
                origin="São Paulo - SP",
                destination="Campinas - SP",
                distance_km=95.0,
                start_date=datetime.now() - timedelta(days=3),
                end_date=datetime.now() - timedelta(days=3),
                vehicle_id=vehicles[1].id,
                driver_id=drivers[1].id,
                status=TripStatus.CONCLUIDA
            ),
            Trip(
                origin="São Paulo - SP",
                destination="Santos - SP",
                distance_km=72.0,
                start_date=datetime.now() - timedelta(days=2),
                vehicle_id=vehicles[2].id,
                driver_id=drivers[2].id,
                status=TripStatus.EM_ANDAMENTO
            ),
            Trip(
                origin="Campinas - SP",
                destination="Ribeirão Preto - SP",
                distance_km=180.0,
                start_date=datetime.now() - timedelta(days=1),
                end_date=datetime.now() - timedelta(hours=12),
                vehicle_id=vehicles[0].id,
                driver_id=drivers[0].id,
                status=TripStatus.CONCLUIDA
            ),
            Trip(
                origin="São Paulo - SP",
                destination="Belo Horizonte - MG",
                distance_km=586.0,
                start_date=datetime.now() + timedelta(days=1),
                vehicle_id=vehicles[3].id,
                driver_id=drivers[4].id,
                status=TripStatus.PLANEJADA
            ),
            Trip(
                origin="Rio de Janeiro - RJ",
                destination="São Paulo - SP",
                distance_km=430.5,
                start_date=datetime.now() - timedelta(days=10),
                end_date=datetime.now() - timedelta(days=9),
                vehicle_id=vehicles[1].id,
                driver_id=drivers[1].id,
                status=TripStatus.CONCLUIDA
            ),
            Trip(
                origin="São Paulo - SP",
                destination="Curitiba - PR",
                distance_km=408.0,
                start_date=datetime.now() - timedelta(days=7),
                end_date=datetime.now() - timedelta(days=6),
                vehicle_id=vehicles[2].id,
                driver_id=drivers[2].id,
                status=TripStatus.CONCLUIDA
            ),
        ]
        db.add_all(trips)
        db.commit()
        print(f"✓ Added {len(trips)} trips")
        
        print("\n✅ Sample data added successfully!")
        print("\nSummary:")
        print(f"  - Vehicles: {db.query(Vehicle).count()}")
        print(f"  - Drivers: {db.query(Driver).count()}")
        print(f"  - Trips: {db.query(Trip).count()}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error adding sample data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_data()
