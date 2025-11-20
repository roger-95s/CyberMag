"""Module providing database models and functions."""

from pathlib import Path
from requests import Session
from sqlalchemy import create_engine, Column, Integer, String, Text, inspect, ForeignKey
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


# Verify if the database is initialized
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


# report table model
class Report(Base):
    """Class representing a report in the database."""

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    site_name = Column(
        String(100),
        ForeignKey("website_fetch.site_name", ondelete="CASCADE"),
        nullable=False,
    )
    title = Column(
        String(255),
        ForeignKey("website_fetch.title", ondelete="CASCADE"),
        nullable=False,
    )
    url = Column(
        String(500),
        ForeignKey("website_fetch.url", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    # content = Column(Text, ForeignKey("article_content.content")
    # , cascade="all, delete", nullable=True)
    analysis = Column(
        Text, ForeignKey("llm_analysis.analysis", ondelete="CASCADE"), nullable=True
    )
    summary = Column(
        Text, ForeignKey("llm_analysis.summary", ondelete="CASCADE"), nullable=True
    )
    risk_level = Column(
        String(50),
        ForeignKey("llm_analysis.risk_level", ondelete="CASCADE"),
        nullable=True,
    )
    created_at = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Report(id={self.id}, title={self.title}, site_name={self.site_name}, url={self.url}, analysis={self.analysis}, summary={self.summary}, risk_level={self.risk_level})>"


# Build table website fetch
class WebsiteFetch(Base):
    """
    Table to store website fetched information,
    after using scraper.py
    Columns {Id, Title, siteName, url}.
    """

    __tablename__ = "website_fetch"

    id = Column(Integer, primary_key=True, index=True)
    site_name = Column(String, index=True)
    title = Column(String, index=True)
    url = Column(String, unique=True, index=True)

    # Save function to store the site_names, titles, and urls in the database to be use for ai analysis
    def save(self):
        """
        Saves site_names, titles, and urls into the database.
        report_data should be a dictionary with
        keys: site_name, title, url.
        """
        session = SessionLocal()
        try:
            # Existence check point if the site_name or title or url already exists
            exists = (
                session.query(WebsiteFetch)
                .filter_by(
                    site_name=self.site_name,
                    title=self.title,
                    url=self.url,
                )
                .first()
            )
            # If true print site_name and title exists
            if exists:
                print(
                    f"⚠️ WebsiteFetch already exists: {self.site_name}: {self.title}"
                )

            # If fetched sites info doesn't exist, create and add the new record
            new_website = WebsiteFetch(self)
            session.add(new_website)
            session.commit()
            # session.refresh(new_website)
            print(f"✅ Success WebsiteFetch was saved: {self.site_name}: {self.title}")
        except ImportError as e:
            print(f"❌ Error saving website fetch: {e}")
            session.rollback()
        finally:
            session.close()

    # Representation method for easier
    # debugging and logging
    def __repr__(self):
        return f"<WebsiteFetch(id={self.id}, title={self.title}, site_name={self.site_name}, url={self.url})>"


# Function that returns all stored websites_fetch and article_content as a list of dicts
def get_all_site():
    """
    Returns all stored websites_fetch and article_content as a list of dicts.
    """
    session = SessionLocal()
    websites = session.query(
        WebsiteFetch
    ).all()  # update session.query to acept multiple arguments
    session.close()

    return [
        {
            "id": r.id,
            "site_name": r.site_name,
            "title": r.title,
            "url": r.url,
            # "analysis": r.analysis,
            # "summary": r.summary,
            # "risk_level": r.risk_level,
        }
        for r in websites
    ]
