from database import init_db, SessionLocal, User, Role
from auth import hash_password

def seed_data():
    init_db()
    db = SessionLocal()
    
    # Check if admin exists
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        print("Creating admin user...")
        hashed_pwd = hash_password("pmnp@123")
        new_admin = User(username="admin", password=hashed_pwd, role=Role.ADMIN)
        db.add(new_admin)
        db.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")
    
    db.close()

if __name__ == "__main__":
    seed_data()
