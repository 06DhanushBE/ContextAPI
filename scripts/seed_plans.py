from app.db.base import SessionLocal
from app.db.models import Plan

def seed():
    db = SessionLocal()

    if db.query(Plan).count() > 0:
        return

    plans = [
        Plan(
            name="free",
            max_ingested_chars=1_000_000,
            max_stored_chars=2_000_000,
            max_chat_tokens=50_000,
        ),
        Plan(
            name="pro",
            max_ingested_chars=20_000_000,
            max_stored_chars=50_000_000,
            max_chat_tokens=2_000_000,
        ),
    ]

    db.add_all(plans)
    db.commit()
    db.close()
    print("Plans seeded")

if __name__ == "__main__":
    seed()
