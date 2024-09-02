from datetime import datetime
from sqlalchemy.sql import func, extract

from models import MonthlyWinner, Score, User

def format_message(template, winner_name, loser_name=None):
    if "[Winner]" in template:
        template = template.replace("[Winner]", winner_name)
    if "[Loser]" in template and loser_name:
        template = template.replace("[Loser]", loser_name)
    return template

def get_current_month_and_year():
    first_day_of_current_month = datetime.now().replace(day=1) 
    current_month = first_day_of_current_month.month
    current_year = first_day_of_current_month.year
    return current_month, current_year

def get_daily_winner(session, date):
    winner = session.query(Score).filter(Score.date == date).order_by(Score.rank).first()
    winner_name = session.query(User).filter_by(id=winner.user_id).first().username
    return winner_name

def get_daily_loser(session, date):
    loser = session.query(Score).filter(Score.date == date).order_by(Score.rank.desc()).first()
    loser_name = session.query(User).filter_by(id=loser.user_id).first().username
    return loser_name

def get_monthly_winner(session, last_month, current_year):
    winner = session.query(MonthlyWinner).filter(
        extract('year', MonthlyWinner.month) == current_year,
        extract('month', MonthlyWinner.month) == last_month
    ).first()
    winnerUsername = session.query(User).filter_by(id=winner.user_id).first().username
    return winnerUsername

def get_monthly_scores(session, last_month, current_year):
    monthly_scores = session.query(
        User.username,
        func.count(Score.id).label('wins')
    ).join(User).filter(
        extract('year', Score.date) == current_year,
        extract('month', Score.date) == last_month
    ).group_by(User.username).order_by(func.count(Score.id).desc()).all()

    return "\n".join([f"{user}: {wins} wins" for user, wins in monthly_scores])

def get_yearly_winner(session):
    current_year = datetime.now().year
    return session.query(MonthlyWinner.user_id, func.count(MonthlyWinner.id).label('win_count')) \
        .filter(func.extract('year', MonthlyWinner.month) == current_year) \
        .group_by(MonthlyWinner.user_id) \
        .order_by(func.count(MonthlyWinner.id).desc()) \
        .first()
