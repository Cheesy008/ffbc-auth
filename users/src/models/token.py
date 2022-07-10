from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from src.db.base_class import Base


class OutstandingToken(Base):
    __tablename__ = "outstanding_token"

    user_id = Column(Integer, ForeignKey("users.user.id"))
    user = relationship("User", back_populates="outstanding_tokens")

    jti = Column(String, unique=True, index=True, nullable=False)
    token = Column(String, nullable=False)

    expires_at = Column(DateTime())

    blacklist_token = relationship(
        "BlacklistToken", back_populates="outstanding_token", uselist=False
    )


class BlacklistToken(Base):
    __tablename__ = "blacklist_token"

    outstanding_token_id = Column(Integer, ForeignKey("users.outstanding_token.id"))
    outstanding_token = relationship("OutstandingToken", back_populates="blacklist_token")
