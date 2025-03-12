from sqlalchemy.ext.declarative import declarative_base
from src.db import Base

class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()