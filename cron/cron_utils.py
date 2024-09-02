from datetime import datetime, timedelta
from sqlalchemy.sql import extract
from models import User, DailyMultiplier
from utils.groupme import send_birthday_message, send_daily_double_message

def get_last_day_of_month(year, month):
    """Returns the last day of the given month and year."""
    if month == 12:
        return datetime(year, month, 31)
    next_month = datetime(year, month + 1, 1)
    return next_month - timedelta(days=1)

def get_last_day_of_year(year):
    """Returns the last day of the given year."""
    return datetime(year, 12, 31)

def get_multipliers_by_date(session, date=datetime.now().date()):
    """Checks if there is any multiplier for today, including a birthday."""
    
    multipliers_today = session.query(DailyMultiplier).filter_by(date=date).all()
    return multipliers_today

def check_for_birthday(session):
    """Returns a list of users whose birthday is today."""
    today = datetime.now().date()
    return session.query(User).filter(
        extract('month', User.birthday) == today.month,
        extract('day', User.birthday) == today.day
    ).all()

def check_for_birthday_messages(session):
    """Checks for birthday messages and sends them if necessary."""
    birthday_users = check_for_birthday(session)
    if birthday_users:
        send_birthday_message(birthday_users)

def check_for_multiplier_messages(session):
    """Checks for multipliers and sends messages if necessary."""
    # Need to change this to do more than just daily double
    if session.query(DailyMultiplier).filter_by(datetime.now().date()).first() is not None:
        send_daily_double_message()

