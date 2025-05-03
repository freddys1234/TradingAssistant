from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    platforms = relationship("Platform", back_populates="user")

class Platform(Base):
    __tablename__ = "platforms"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    type = Column(String)
    currency = Column(String)
    fee = Column(Float)
    daily_budget = Column(Float, nullable=True)
    user = relationship("User", back_populates="platforms")
    positions = relationship("Position", back_populates="platform")

class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True)
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    entry_price = Column(Float)
    quantity = Column(Integer)
    take_profit = Column(Float)
    stop_loss = Column(Float)
    reentry_price = Column(Float, nullable=True)
    status = Column(Enum("open", "closed", name="position_status"), default="open")
