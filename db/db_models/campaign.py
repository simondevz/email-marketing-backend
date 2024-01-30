from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from datetime import datetime
import uuid as uuid_pkg

from ..database import Base

class CampaignModel(Base):
    __tablename__ = 'campaigns'
    id = Column(UUIDType(binary=True), primary_key=True, default=uuid_pkg.uuid4)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'))
    list_id = Column(Integer, ForeignKey('Lists.id'))
    status = Column(String(50), nullable=False) #  Draft, Scheduled, Sent, etc.
    scheduled_at = Column(TIMESTAMP)
    sent_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    user = relationship('User', backref='campaigns')
    list = relationship('List', backref='campaigns')

class CampaignEmailModel(Base):
    __tablename__ = 'campaign_emails'
    id = Column(UUIDType(binary=True), primary_key=True, default=uuid_pkg.uuid4)
    campaign_id = Column(Integer, ForeignKey('Campaigns.id'))
    subject = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    campaign = relationship('Campaign', backref='emails')

class CampaignInteractionModel(Base):
    __tablename__ = 'campaign_interactions'
    id = Column(UUIDType(binary=True), primary_key=True, default=uuid_pkg.uuid4)
    campaign_id = Column(Integer, ForeignKey('Campaigns.id'))
    subscriber_id = Column(Integer, ForeignKey('Subscribers.id'))
    interaction_type = Column(String(50), nullable=False) #Open, Click, etc.
    interaction_time = Column(TIMESTAMP, server_default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    campaign = relationship('Campaign', backref='interactions')
    subscriber = relationship('Subscriber', backref='interactions')