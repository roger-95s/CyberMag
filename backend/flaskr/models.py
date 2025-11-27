from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class ReportCard(db.Model):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    site_name: Mapped[str] = mapped_column(String(100), index=True)

    title: Mapped[str] = mapped_column(String(500), nullable=False)

    url: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    
    analysis: Mapped[str] = mapped_column(Text, nullable=True)
    
    summary: Mapped[str] = mapped_column(Text, nullable=True)
    
    risk_level: Mapped[str] = mapped_column(String(50), nullable=True)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)


class WebsiteFetch(db.Model):
    __tablename__ = "website_fetch"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    site_name: Mapped[str] = mapped_column(String(100), index=True)
    
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    
    url: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)

    def to_dict(self):
        """Helper to convert model to dictionary for JSON responses"""
        return {
            "id": self.id,
            "site_name": self.site_name,
            "title": self.title,
            "url": self.url
        }