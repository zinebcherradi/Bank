from config import engine, Base
import entities

def reset_db():
    print("Dropping all tables...")
    # Drop in order: transactions -> accounts -> users
    Base.metadata.drop_all(engine)
    print("Tables dropped. Recreating...")
    Base.metadata.create_all(engine)
    print("Database reset complete.")

if __name__ == "__main__":
    reset_db()
