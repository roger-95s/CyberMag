"""Module providing database models and functions."""

from pathlib import Path
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

    # save method to add a new website fetch record
    def save(self):
        """
        Saves a report to the database.
        report_data should be a dictionary with
        keys: title, url, summary, risk_level.
        """
        session = SessionLocal()
        try:
            # Existence check point if the record already exists
            exists = (
                session.query(WebsiteFetch)
                .filter_by(
                    site_name=self["site_name"],
                    title=self["title"],
                    url=self["url"],
                )
                .first()
            )
            # If it exists, print a message and return
            if exists:
                print(
                    f"⚠️ WebsiteFetch already exists: {self['site_name']}: {self['title']}"
                )
                return self

            # If it doesn't exist, create and add the new record
            new_website = WebsiteFetch(**self)
            session.add(new_website)
            session.commit()
            # session.refresh(new_website)
            print(f"✅ WebsiteFetch saved: {self['site_name']}: {self['title']}")
        except ImportError as e:
            print(f"❌ Error saving website fetch: {e}")
            session.rollback()
        finally:
            session.close()
        return self

    # Representation method for easier
    # debugging and logging
    def __repr__(self):
        return f"<WebsiteFetch(id={self.id}, title={self.title}, site_name={self.site_name}, url={self.url})>"


# Table web articles content
class ArticleContent(Base):
    """
    Table to store article content after fetched from content.py
    Columns {ForeignKey, content}.
    """

    __tablename__ = "article_content"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=True)

    # save method to add a new website fetch record
    def save(self):
        """
        Saves a report to the database.
        report_data should be a dictionary with
        keys: title, url, summary, risk_level.
        """
        session = SessionLocal()
        try:
            # Existence check point
            exists = (
                session.query(ArticleContent)
                .filter_by(
                    content=self["content"],
                )
                .first()
            )
            # If it exists, print a message and return
            if exists:
                print(f"⚠️ WebsiteFetch already exists: {self}")
                return self
            # If it not in report create a new report
            new_content = ArticleContent(**self)
            session.add(new_content)
            session.commit()
            print(f"✅ Content Saved to DB: {new_content}...")

        except ImportError as e:
            print(f"❌ Error saving report: {e}")
            session.rollback()
        finally:
            session.close()
        return self

    def __repr__(self):
        return f"<ArticleContent(id={self.id}, content={self.content})>"


# Table LLM Analysis and Summary
class LLManalysis(Base):
    """
    Table to store LLM analysis and summary
    Columns {ForeignKey, analysis, summary, risk_level}.
    """

    __tablename__ = "llm_analysis"

    id = Column(Integer, primary_key=True, index=True)
    # article_content = Column(Integer, ForeignKey("article_content.content"),
    # cascade="all, delete", nullable=False)
    analysis = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    risk_level = Column(String(50), nullable=True)

    def __repr__(self):
        return f"<LLMAnalysis(id={self.id}, analysis={self.analysis}, summary={self.summary} risk_level={self.risk_level})>"


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
