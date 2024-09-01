from sqlalchemy import Column, Integer, String, Interval, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Base class for all models
Base = declarative_base()

# Users table model
class User(Base):
    __tablename__ = 'Users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), unique=True, nullable=False)
    username = Column(String(100), nullable=False)
    
    scores = relationship('Score', back_populates='user')

class Score(Base):
    __tablename__ = 'Scores'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    score_time = Column(Interval, nullable=False)
    rank = Column(Integer, nullable=True)
    date = Column(Date, nullable=False)
    
    user = relationship('User', back_populates='scores')

class MonthlyWinner(Base):
    __tablename__ = 'MonthlyWinners'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    wins = Column(Integer, nullable=False)
    month = Column(Date, nullable=False)
    
    user = relationship('User')

class DailyMessage(Base):
    __tablename__ = 'DailyMessages'
    
    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)

class MonthlyMessage(Base):
    __tablename__ = 'MonthlyMessages'
    
    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)

class YearlyMessage(Base):
    __tablename__ = 'YearlyMessages'
    
    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)