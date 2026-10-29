from app import create_app, db
from app.models import User

app = create_app()

def seed_users():
    with app.app_context():
        # Ensure fresh tables exist
        db.create_all()

        # Check if users already exist to avoid duplicate inserts
        if User.query.first():
            print("Database already contains user records. Seeding skipped.")
            return

        # 1. Admin User
        admin = User(
            registration_no="ADM/001",
            email="admin@university.ac.ke",
            first_name="System",
            last_name="Administrator",
            role="admin"
        )
        admin.set_password("admin123")

        # 2. Lecturer User
        lecturer = User(
            registration_no="LEC/101",
            email="lecturer@university.ac.ke",
            first_name="Dr. Alan",
            last_name="Turing",
            role="lecturer"
        )
        lecturer.set_password("lec123")

        # 3. Student User
        student = User(
            registration_no="BIT/2024/001",
            email="student@university.ac.ke",
            first_name="John",
            last_name="Doe",
            role="student"
        )
        student.set_password("student123")

        # Stage and commit to MySQL
        db.session.add_all([admin, lecturer, student])
        db.session.commit()

        print("Database successfully seeded with Admin, Lecturer, and Student test accounts!")

if __name__ == "__main__":
    seed_users()