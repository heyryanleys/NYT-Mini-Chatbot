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
    
    # Relationship to Scores
    scores = relationship('Score', back_populates='user')

# Scores table model
class Score(Base):
    __tablename__ = 'Scores'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    score_time = Column(Interval, nullable=False)
    rank = Column(Integer, nullable=True)  # Adding rank column
    date = Column(Date, nullable=False)
    
    # Relationship to User
    user = relationship('User', back_populates='scores')

# MonthlyWinners table model
class MonthlyWinner(Base):
    __tablename__ = 'MonthlyWinners'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    wins = Column(Integer, nullable=False)
    month = Column(Date, nullable=False)
    
    # Relationship to User
    user = relationship('User')
