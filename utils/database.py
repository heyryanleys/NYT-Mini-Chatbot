from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import config
from datetime import datetime
from models import User, Score

def create_session():
    DATABASE_URL = config.DATABASE_URL
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def save_users_to_db(session, data):
    for user_data in data.get("data", []):
        user_id = str(user_data.get("userID"))
        username = user_data.get("name")
        if user_id and username:
            add_user_if_not_exists(session, user_id, username)

def save_scores_to_db(session, data):
    for score in data.get("scoreList", []):
        username = score.get("name")
        solve_time = score.get("solveTime")
        rank = score.get("rank")
        user = session.query(User).filter_by(username=username).first()
        if user and solve_time:
            # check if a score already exists for that user for that date 
            existing_score = session.query(Score).filter_by(user_id=user.id, date=datetime.now().date()).first()
            if existing_score is None:
                new_score = Score(user_id=user.id, score_time=solve_time, date=datetime.now(), rank=rank)
                session.add(new_score)
                session.commit()

def save_multiplier_to_score(session, user_id, multiplier):
    score = session.query(Score).filter_by(user_id=user_id).first()
    if score:
        score.multiplier = multiplier
        session.commit()

def add_user_if_not_exists(session, user_id, username):
    user = session.query(User).filter_by(user_id=user_id).first()
    if not user:
        user = User(user_id=user_id, username=username)
        session.add(user)
        session.commit()
