import requests
from sqlalchemy.sql import func
from models import DailyMessage, MonthlyMessage, YearlyMessage
from utils.messages import format_message, get_current_month_and_year, get_monthly_winner, get_monthly_scores, get_yearly_winner, get_daily_winner, get_daily_loser
import config
from datetime import datetime

def send_groupme_message(message):
    url = 'https://api.groupme.com/v3/bots/post'
    data = {
        "bot_id": config.bot_id,
        "text": message
    }
    response = requests.post(url, json=data)
    if response.status_code != 202:
        print(f"Failed to send message: {response.status_code}")
        print(response.json())

def send_groupme_daily_message(session):
    today = datetime.now().date()
    daily_message = session.query(DailyMessage).order_by(func.random()).first().message
    winner_name = get_daily_winner(session, today)
    loser_name = get_daily_loser(session, today)

    message = format_message(daily_message, winner_name, loser_name)
    send_groupme_message(message)

def send_groupme_monthly_message(session):
    current_month, current_year = get_current_month_and_year()
    monthly_winner = get_monthly_winner(session, current_month, current_year)
    
    formatted_scores = get_monthly_scores(session, current_month, current_year)
    monthly_message = session.query(MonthlyMessage).order_by(func.random()).first().message

    message = format_message(monthly_message, monthly_winner, None)
    send_groupme_message(f"{message}\n\nScores:\n{formatted_scores}")

def send_groupme_yearly_message(session):
    yearly_winner = get_yearly_winner(session)
    yearly_message = session.query(YearlyMessage).order_by(func.random()).first().message

    message = format_message(yearly_message, yearly_winner, None)
    send_groupme_message(message)

def send_birthday_message(users):
    if len(users) > 1: 
        if len(users) == 2:
            # For two users, join their names with "and"
            usernames = f"{users[0].username} and {users[1].username}"
        else:
            # For more than two users, join names with commas and "and" before the last name
            usernames = ", ".join(user.username for user in users[:-1])
            usernames += f", and {users[-1].username}"

        message = f"Happy Birthday {usernames}! 🎉🎂 \n\nIf one of you wins today, it's worth triple points!"
    else: 
        user = users[0]
        message = f"Happy Birthday, {user.username}! 🎉🎂\n\nIf you win today, it's worth triple points!"

    send_groupme_message(message)

def send_daily_double_message():
    send_groupme_message("Today is a Daily Double! All scores are worth double points!")
