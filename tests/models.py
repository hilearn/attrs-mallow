from typing import List

from marshmallow_helpers.model import model_with_schema

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, JSON
from sqlalchemy.ext.declarative import declarative_base, declared_attr


Base = declarative_base()


class USAStatesMixin:
    abbreviation = Column(String, primary_key=True)
    name = Column(String)


@model_with_schema
class StatesData(Base, USAStatesMixin):
    __tablename__ = 'usa_state'


class Zcta5Mixin:
    geometry = Column(JSON)

    @declared_attr
    def state(self) -> str:
        return Column(String,
                      ForeignKey('usa_state.abbreviation'),
                      nullable=False)


@model_with_schema
class Zcta5(Base, Zcta5Mixin):
    __tablename__ = 'usa_zcta5'
    zcta = Column(String, primary_key=True)


@model_with_schema
class Table(Base):
    __tablename__ = 'table'
    column = Column(String, primary_key=True)
    dictionary = Column(JSON)
    array: List[str] = Column(JSON)
