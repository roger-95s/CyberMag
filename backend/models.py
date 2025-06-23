from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database location
DATABASE_URL = "sqlite:///cybermag.db"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base() 

# Report table model
class Report(Base):
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
    Base.metadata.create_all(bind=engine)

# Save a report 
def save_report(report_data):
    """
    Saves a report to the database.
    report_data should be a dictionary with keys: title, url, summary, risk_level.
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
    except Exception as e:
        print(f"❌ Error saving report: {e}")
        session.rollback()
    finally:
        session.close()

# Fetch all reports
def get_all_reports():
    """
    Returns all stored reports as a list of dicts.
    """
    session = SessionLocal()
    reports = session.query(Report).all()
    session.close()

    return [{
        "id": r.id,
        "title": r.title,
        "url": r.url,
        "content": r.content,
        "analysis": r.analysis,
        "summary": r.summary,
        "risk_level": r.risk_level
    } for r in reports]
