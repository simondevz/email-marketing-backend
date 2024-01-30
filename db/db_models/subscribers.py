from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from datetime import datetime
import uuid as uuid_pkg

from ..database import Base

class ListModel(Base):
    __tablename__ = 'lists'
    id = Column(UUIDType(binary=True), primary_key=True, default=uuid_pkg.uuid4)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'))
    created_at = Column(TIMESTAMP, server_default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    user = relationship('User', backref='lists')

class SubscriberModel(Base):
    __tablename__ = 'subscribers'
    id = Column(UUIDType(binary=True), primary_key=True, default=uuid_pkg.uuid4)
    email = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    list_id = Column(Integer, ForeignKey('Lists.id'))
    created_at = Column(TIMESTAMP, server_default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    list = relationship('List', backref='subscribers')