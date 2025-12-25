from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import DateTime, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from typing import Any


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class Cybersecurity_Reports(db.Model):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Add ai tool
    agent_name: Mapped[str] = mapped_column(String(500), index=True)

    # Metadata fields for the report  
    url: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    site_name: Mapped[str] = mapped_column(String(100), index=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    publication_date: Mapped[str] = mapped_column(String(50), nullable=True)
    article_type: Mapped[str] = mapped_column(String(100), nullable=True)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Storing the full analysis payload as JSONB
    analysis_payload: Mapped[dict[str, Any]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"), 
        nullable=False
    )

    # Timestamps for record keeping or DB-level timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=db.func.now())


    def to_dict(self):
        return {
            "id": self.id,
            "site_name": self.site_name,
            "title": self.title,
            "url": self.url, 
            'summary': self.summary,
        } 


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
    

