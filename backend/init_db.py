"""
Initialize database with admin user.
"""
from sqlalchemy.orm import Session
from database.session import engine, Base, get_db
from models.user import User
from models.agent import AgentJob  # Import to register table with SQLAlchemy
from core.security import get_password_hash
from core.config import settings

def init_db():
    """Initialize database with tables and admin user."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("[OK] Database tables created")

    # Create database session
    db = next(get_db())

    try:
        # Check if admin user already exists
        admin = db.query(User).filter(User.email == settings.FIRST_SUPERUSER_EMAIL).first()

        if admin:
            print(f"[OK] Admin user already exists: {settings.FIRST_SUPERUSER_EMAIL}")
        else:
            # Create admin user
            admin = User(
                email=settings.FIRST_SUPERUSER_EMAIL,
                hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                full_name="System Administrator",
                role="knowledge_engineer",
                is_active=True,
                is_superuser=True,
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print(f"[OK] Created admin user: {settings.FIRST_SUPERUSER_EMAIL}")
            print(f"  Password: {settings.FIRST_SUPERUSER_PASSWORD}")
            print(f"  Role: knowledge_engineer (superuser)")

        # Create demo users for testing
        demo_users = [
            {
                "email": "teacher@example.com",
                "password": "teacher123",
                "full_name": "Demo Teacher",
                "role": "teacher",
            },
            {
                "email": "author@example.com",
                "password": "author123",
                "full_name": "Demo Author",
                "role": "author",
            },
            {
                "email": "editor@example.com",
                "password": "editor123",
                "full_name": "Demo Editor",
                "role": "editor",
            },
        ]

        print("\nCreating demo users...")
        for user_data in demo_users:
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing:
                user = User(
                    email=user_data["email"],
                    hashed_password=get_password_hash(user_data["password"]),
                    full_name=user_data["full_name"],
                    role=user_data["role"],
                    is_active=True,
                    is_superuser=False,
                )
                db.add(user)
                db.commit()
                print(f"[OK] Created {user_data['role']}: {user_data['email']} / {user_data['password']}")
            else:
                print(f"  {user_data['role']}: {user_data['email']} (already exists)")

        print("\n" + "="*60)
        print("Database initialization complete!")
        print("="*60)
        print("\nLogin Credentials:")
        print(f"\nAdmin:")
        print(f"  Email: {settings.FIRST_SUPERUSER_EMAIL}")
        print(f"  Password: {settings.FIRST_SUPERUSER_PASSWORD}")
        print(f"\nDemo Users:")
        print(f"  Teacher: teacher@example.com / teacher123")
        print(f"  Author: author@example.com / author123")
        print(f"  Editor: editor@example.com / editor123")
        print("\n" + "="*60)

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
