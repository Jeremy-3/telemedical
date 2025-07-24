from app import app
from models import db, User
from datetime import date

def seed_data():
    # Delete all existing users
    db.session.query(User).delete()

    # Create default users
    admin_user = User(username="Admin", email="admin@gmail.com", role="admin")
    admin_user.set_password("SuperAdmin")  # Hash password properly

    db.session.add(admin_user)  # Add user to the session
    db.session.commit()

    print("Database seeded successfully!")

# Run inside application context
with app.app_context():
    seed_data()
