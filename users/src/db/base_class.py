from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)

    __table_args__ = {"schema": "users"}
