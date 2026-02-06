"""
Script to verify database tables and user data
"""
from sqlmodel import select
from database.database import engine, get_session
from models.user import User
from models.task import Task

def verify_tables():
    """Verify that both User and Task tables exist in the database"""
    print("Verifying database tables...")

    # Import the models to ensure they're registered with SQLModel
    from models.user import User
    from models.task import Task

    # Check if tables exist by trying to create them (won't recreate if exist)
    try:
        User.metadata.create_all(bind=engine)
        Task.metadata.create_all(bind=engine)
        print("+ Tables verified/created successfully")
    except Exception as e:
        print(f"- Error creating tables: {e}")
        return False

    return True

def list_users():
    """List all users in the database"""
    print("\nListing all users in the database...")

    try:
        session_gen = get_session()
        session = next(session_gen)
        try:
            users = session.exec(select(User)).all()
            if users:
                for user in users:
                    print(f"- User ID: {user.id}, Email: {user.email}, Name: {user.name}")
            else:
                print("No users found in database")

            print(f"Total users: {len(users)}")
        finally:
            # Close the session properly
            session.close()
    except Exception as e:
        print(f"- Error listing users: {e}")
        return False

    return True

def main():
    print("Database Verification Script")
    print("=" * 30)

    # Verify tables exist
    if not verify_tables():
        return False

    # List existing users
    list_users()

    print("\nVerification complete!")

if __name__ == "__main__":
    main()