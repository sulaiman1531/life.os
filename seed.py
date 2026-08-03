import asyncio
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models

# Ensure all tables are created
Base.metadata.create_all(bind=engine)

def seed_db():
    db = SessionLocal()
    try:
        # Check if user already exists
        user = db.query(models.User).filter(models.User.email == "test@example.com").first()
        if not user:
            print("Creating default user...")
            hashed_password = "password" + "notreallyhashed"
            user = models.User(
                email="test@example.com",
                full_name="Admin User",
                hashed_password=hashed_password
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"Default user created successfully! ID: {user.id}")
        else:
            print(f"Default user already exists. ID: {user.id}")
            
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
