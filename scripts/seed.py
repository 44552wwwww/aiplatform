"""Seed database with demo data for development / showcase.

Usage:
    cd backend && python ../scripts/seed.py
    # or from project root:
    python scripts/seed.py
"""

import sys
from pathlib import Path

# Ensure backend/ is on sys.path so we can import app modules
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.database.base import Base
from app.database.database import engine
from app.models.user import User
from app.models.report import Report
from app.core.security import hash_password
from sqlalchemy.orm import Session


def seed():
    """Create demo data."""
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        # Check if demo user already exists
        existing = db.query(User).filter(User.username == "demo").first()
        if existing:
            print("[SKIP] Demo user already exists (username: demo)")
        else:
            demo_user = User(
                username="demo",
                password_hash=hash_password("demo123"),
            )
            db.add(demo_user)
            db.commit()
            print("[OK] Created demo user: username=demo, password=demo123")

        # Summary
        user_count = db.query(User).count()
        report_count = db.query(Report).count()
        print(f"[INFO] Database summary: {user_count} users, {report_count} reports")


if __name__ == "__main__":
    seed()
