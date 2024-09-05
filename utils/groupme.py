import requests
from sqlalchemy.sql import func
from models import DailyMessage, MonthlyMessage, YearlyMessage
from utils.messages import format_daily_message, get_last_month_and_year, format_monthly_message, format_yearly_message
from utils.database import get_monthly_scores, get_yearly_scores, get_daily_scores
import config
from datetime import datetime

def send_groupme_message(message, picture=None):
    url = 'https://api.groupme.com/v3/bots/post'
    data = {
        "bot_id": config.bot_id,
        "text": message,
        "picture_url": picture
    }
    response = requests.post(url, json=data)
    if response.status_code != 202:
        print(f"Failed to send message: {response.status_code}")
        print(response.json())

def send_groupme_daily_message(session):
    today = datetime.now().date()
    daily_scores = get_daily_scores(session, today)
    daily_message = session.query(DailyMessage).order_by(func.random()).first().message

    if (len(daily_scores) == 0):
        message = "No competitors today? Sad... Get it together, people!"
    else:
        message = format_daily_message(daily_message, daily_scores)

    

    send_groupme_message(message)

def send_groupme_monthly_message(session):
    last_month, last_year = get_last_month_and_year()
    
    monthly_scores = get_monthly_scores(session, last_month, last_year)
    
    monthly_message = session.query(MonthlyMessage).order_by(func.random()).first().message

    if (len(monthly_scores) == 0):
        message = "No competitors this month? It's like you don't even care!"
    else:
        message = format_monthly_message(monthly_message, monthly_scores)

    send_groupme_message(message)

def send_groupme_yearly_message(session):
    # Use the current year and subtract one
    current_year = datetime.now().year
    last_year = current_year - 1
    
    yearly_scores = get_yearly_scores(session, last_year)
    yearly_message = session.query(YearlyMessage).order_by(func.random()).first().message

    if (len(yearly_scores) == 0):
        message = "I can't believe it! No one competed all year! 😱"
    else:
        message = format_yearly_message(yearly_message, yearly_scores)

    send_groupme_message(message)

def send_groupme_birthday_message(users):
    if len(users) > 1: 
        if len(users) == 2:
            # For two users, join their names with "and"
            usernames = f"{users[0].username} and {users[1].username}"
        else:
            # For more than two users, join names with commas and "and" before the last name
            usernames = ", ".join(user.username for user in users[:-1])
            usernames += f", and {users[-1].username}"

        message = f"Happy Birthday {usernames}! 🎉🎂 \nIf one of you wins today, it's worth triple points!"
    else: 
        user = users[0]
        message = f"Happy Birthday, {user.username}! 🎉🎂\nIf you win today, it's worth triple points!"

    send_groupme_message(message, "https://i.groupme.com/1378x776.png.c1898eaad0ea4e80af773be311d8c8fd")

def send_groupme_daily_double_message():
    send_groupme_message("🚨 Today is a Daily Double! The winner of today earns double the points! 🚨", "https://i.groupme.com/2388x1246.png.6592f889a1d143fbb714cbff5b1f4040")
