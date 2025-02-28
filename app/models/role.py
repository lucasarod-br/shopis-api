from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    users = relationship('User', back_populates='role')

    @staticmethod
    def seed(session):
        roles = [
            Role(name='user'),
            Role(name='admin')
        ]
        session.add_all(roles)
        session.commit()