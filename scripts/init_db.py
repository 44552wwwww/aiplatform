"""Initialize database tables."""

from app.database.base import Base
from app.database.database import engine


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")


if __name__ == "__main__":
    init_db()
