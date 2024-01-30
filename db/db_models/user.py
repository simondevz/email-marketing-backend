from datetime import datetime
from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
import uuid as uuid_pkg

from ..database import Base

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(UUIDType(binary=True), primary_key=True, default=uuid_pkg.uuid4)
    username: str = Column(String(255), nullable=False)
    email: str = Column(String(255), nullable=False)
    password_hash: str = Column(String(255), nullable=False)
    created_at: datetime = Column(TIMESTAMP, server_default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # last_login: datetime === add latter

