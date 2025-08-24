"""Module providing database models and functions."""

from pathlib import Path
from sqlalchemy import Column, Integer, String, Text, DateTime, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Using absolute path for the database file
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "cybermag.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    url = Column(String(500), unique=True, nullable=False)
    summary = Column(Text, nullable=True)
    risk_level = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())



Base.metadata.create_all(bind=engine)


def save_report(report_data):
    """
    Guarda un reporte en la base de datos.
    report_data debe ser un diccionario con
    keys: title, url, summary, risk_level
    """
    session = SessionLocal()
    try:
        exists = session.query(Report).filter_by(url=report_data["url"]).first()
        if exists:
            print(f"⚠️ Report already exists: {report_data['title']}")
            return

        new_report = Report(**report_data)
        session.add(new_report)
        session.commit()
        print(f"✅ Saved to DB: {new_report.title}")
    except Exception as e:
        print(f"❌ Error saving report: {e}")
        session.rollback()
    finally:
        session.close()


def get_all_reports():
    """
    Returns all stored reports as a list of dicts.
    """
    session = SessionLocal()
    reports = session.query(Report).all()
    session.close()

    return [
        {
            "id": r.id,
            "title": r.title,
            "url": r.url,
            "summary": r.summary,
            "risk_level": r.risk_level,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in reports
    ]
