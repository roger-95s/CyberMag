"""Module providing a functions python version."""

from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Text, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


# Using absolute path for the database file
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "cybermag.db"
# SQLite database location
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# Report table model
class Report(Base):
    """Class representing a report in the database."""

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False, unique=True)
    content = Column(Text, nullable=True)
    analysis = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    risk_level = Column(String(50), nullable=True)


# Create tables if not already created
def init_db():
    """Function initializing database table. Run it once to create the database."""

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database initialized at {DATABASE_PATH}")

    # Verify if the table exists
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables in the database: {tables}")


def verify_db():
    """Function to verify if the database is initialized."""

    if not DATABASE_PATH.exists():
        print(
            f"❌ Database file does not exist at {DATABASE_PATH}. Please run init_db() first."
        )
        return False

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if "reports" not in tables:
        print(
            f"❌ 'reports' table does not exist. {tables} Please run init_db() first."
        )
        return False

    print(f"✅ Database is initialized and 'reports': {DATABASE_PATH} table exists.")
    return True


# Save a report
def save_report(report_data):
    """
    Saves a report to the database.
    report_data should be a dictionary with
    keys: title, url, summary, risk_level.
    """
    session = SessionLocal()
    try:
        # Prevent duplicates inside this function
        exists = session.query(Report).filter_by(url=report_data["url"]).first()
        if exists:
            print(f"⚠️ Report already exists: {report_data['title']}")
            return

        new_report = Report(**report_data)
        session.add(new_report)
        session.commit()
        print(f"✅ Saved to DB: {new_report.title}")
    except ImportError as e:
        print(f"❌ Error saving report: {e}")
        session.rollback()
    finally:
        session.close()


# Get all reports
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
            "content": r.content,
            "analysis": r.analysis,
            "summary": r.summary,
            "risk_level": r.risk_level,
        }
        for r in reports
    ]
