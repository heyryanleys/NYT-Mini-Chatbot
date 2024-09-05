from datetime import datetime
from sqlalchemy.sql import func, extract
from dateutil.relativedelta import relativedelta

from models import Score, User

def format_daily_message(template, daily_scores):

    winner_name = daily_scores[0][1]  # Username is at index 1
    loser_name = daily_scores[-1][1]  # Username is at index 1

    if "[Winner]" in template:
        template = template.replace("[Winner]", winner_name)
    if "[Loser]" in template and loser_name:
        template = template.replace("[Loser]", loser_name)

    return template

def format_monthly_message(template, monthly_scores):
    print(monthly_scores)
    
    winner_name = monthly_scores[0][1]  # Username is at index 1
    loser_name = monthly_scores[-1][1]  # Username is at index 1

    if "[Winner]" in template:
        template = template.replace("[Winner]", winner_name)
    if "[Loser]" in template and loser_name:
        template = template.replace("[Loser]", loser_name)

    formatted_scores = "\n".join([f"{username}: {points}" for _, username, points in monthly_scores])

    return template + "\n\nScores:\n" + formatted_scores

def format_yearly_message(template, yearly_scores):
    winner_name = yearly_scores[0][1]  # Username is at index 1
    loser_name = yearly_scores[-1][1]  # Username is at index 1

    if "[Winner]" in template:
        template = template.replace("[Winner]", winner_name)
    if "[Loser]" in template and loser_name:
        template = template.replace("[Loser]", loser_name)

    formatted_scores = "\n".join([f"{username}: {points}" for _, username, points in yearly_scores])

    return template + "\n\nScores:\n" + formatted_scores


def get_last_month_and_year():
    # Subtract one month from the current date
    last_month_date = datetime.now() - relativedelta(months=1)
    return last_month_date.month, last_month_date.year

def get_daily_scores(session, date):
    result = session.query(
        User.user_id,
        User.username,
        func.sum(Score.points).label('total_points')
    ).join(Score, User.id == Score.user_id) \
     .filter(Score.date == date) \
     .group_by(User.user_id, User.username) \
     .order_by(func.sum(Score.points).desc()) \
     .all()

    return result

def get_monthly_scores(session, month, year):
    result = session.query(
        User.user_id,
        User.username,
        func.sum(Score.points).label('total_points')
    ).join(Score, User.id == Score.user_id) \
     .filter(
         extract('year', Score.date) == year,
         extract('month', Score.date) == month
     ) \
     .group_by(User.user_id, User.username) \
     .order_by(func.sum(Score.points).desc()) \
     .all()

    return result

def get_yearly_scores(session, year):
    result = session.query(
        User.user_id,
        User.username,
        func.sum(Score.points).label('total_points')
    ).join(Score, User.id == Score.user_id) \
     .filter(extract('year', Score.date) == year) \
     .group_by(User.user_id, User.username) \
     .order_by(func.sum(Score.points).desc()) \
     .all()

    return result