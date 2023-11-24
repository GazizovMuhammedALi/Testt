from sqlalchemy import Column, Integer, String, Text, Date, BLOB, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import datetime

Base = declarative_base()


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)

    services = relationship("Service", backref="category")


class Service(Base):
    __tablename__ = "service"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    category_id = Column(ForeignKey("category.id"))


class LastWork(Base):
    __tablename__ = "last_work"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=datetime.date.today())
    image = Column(BLOB)


def create_tables(engine):
    Base.metadata.create_all(engine, checkfirst=True)