from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from src.db.base_class import Base


class User(Base):
    __tablename__ = "user"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    phone = Column(String, nullable=False)

    outstanding_tokens = relationship("OutstandingToken", back_populates="user")
