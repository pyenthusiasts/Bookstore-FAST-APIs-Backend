"""
Book model for database.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base


class Book(Base):
    """Book model."""

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    # Relationships
    author = relationship("Author", back_populates="books")

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title})>"
