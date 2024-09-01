import requests
from sqlalchemy.sql import func
from sqlalchemy import extract
from bs4 import BeautifulSoup
from twilio.rest import Client
from dotenv import load_dotenv
from models import DailyMessage, Score, User, MonthlyWinner, MonthlyMessage, YearlyMessage
import os
import re
import json
from datetime import datetime, timedelta
from models import User, Score

load_dotenv()


bot_id = os.getenv('GROUPME_BOT_ID')  # Ensure this is set in your .env file

def add_user_if_not_exists(session, user_id, username):
    user = session.query(User).filter_by(user_id=user_id).first()
    if not user:
        user = User(user_id=user_id, username=username)
        session.add(user)
        session.commit()
        print(f"Added new user: {username}")
    else :
        print(f"User {username} already exists.")

def save_users_to_db(session, data):
    for user_data in data.get("data", []):
        user_id = str(user_data.get("userID"))
        username = user_data.get("name")
        if user_id and username:
            add_user_if_not_exists(session, user_id, username)
        else:
            print(f"Skipping user with missing id or username: {user_data}")

def get_leaderboard_users(headers):
    url = "https://www.nytimes.com/svc/crosswords/v6/leaderboard/mini.json"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch puzzle data: {response.status_code}")
    return None

def get_daily_scores(headers):
    url = "https://www.nytimes.com/puzzles/leaderboards"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find('script', string=re.compile('window.data'))
    if script:
        json_data = re.search(r'window\.data\s*=\s*(\{.*\});?', script.string, re.DOTALL)
        if json_data:
            data = json.loads(json_data.group(1))
            return data
        else:
            print('Failed to extract JSON data.')
    else:
        print('Script containing window.data not found.')
    return None

def save_scores_to_db(session, data):
    for score in data.get("scoreList", []):
        username = score.get("name")
        solve_time = score.get("solveTime")
        rank = score.get("rank")
        user = session.query(User).filter_by(username=username).first()
        if user and solve_time:
            print(f"Attempting to save score for user_id: {user.id}, username: {username}, solve_time: {solve_time}")
            new_score = Score(user_id=user.id, score_time=solve_time, date=datetime.now(), rank=rank)
            session.add(new_score)
            session.commit()
            print(f"Saved score for {username}: {solve_time}, Rank: {rank}")
        else:
            print(f"Skipping user {username} with no solve time or not found in DB.")

def sendTextMessage():
    
    # Pick a message from the DB
    message = "Hey!"
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH')
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        body="Join Earth's mightiest heroes. Like Kevin Bacon.",
        from_=os.getenv('TWILIO_PHONE_NUMBER'),
        to=os.getenv('TEST_TWILO_SEND_TO')
    )

    print(message.body)


def send_groupme_daily_message(session):

    today = datetime.now().date()

    daily_message = session.query(DailyMessage).order_by(func.random()).first().message


    # Get the winner and loser of the day
    winner = session.query(Score).filter(Score.date == today).order_by(Score.rank).first()
    loser = session.query(Score).filter(Score.date == today).order_by(Score.rank.desc()).first()
    winnerName = session.query(User).filter_by(id=winner.user_id).first().username
    loserName = session.query(User).filter_by(id=loser.user_id).first().username

    # If daily_message has [Winner] in it, replace it with the winner's name
    if "[Winner]" in daily_message:
        daily_message = daily_message.replace("[Winner]", winnerName)

    # If daily_message has [Loser] in it, replace it with the loser's name
    if "[Loser]" in daily_message:
        daily_message = daily_message.replace("[Loser]", loserName)

    # GroupMe API endpoint
    url = 'https://api.groupme.com/v3/bots/post'

    # Payload for the API request
    data = {
        "bot_id": bot_id,
        "text": daily_message
    }

    # Send the request to the GroupMe API
    response = requests.post(url, json=data)

    if response.status_code == 202:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message: {response.status_code}")
        print(response.json())

def get_last_month_and_year():
    first_day_of_current_month = datetime.now().replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    last_month = last_day_of_previous_month.month
    current_year = last_day_of_previous_month.year
    return last_month, current_year

def get_monthly_winner(session, last_month, current_year):
    return session.query(MonthlyWinner).filter(
        extract('year', MonthlyWinner.month) == current_year,
        extract('month', MonthlyWinner.month) == last_month
    ).first()

def get_monthly_scores(session, last_month, current_year):
    monthly_scores = session.query(
        User.username,
        func.count(Score.id).label('wins')
    ).join(User).filter(
        extract('year', Score.date) == current_year,
        extract('month', Score.date) == last_month
    ).group_by(User.username).order_by(func.count(Score.id).desc()).all()

    return "\n".join([f"{user}: {wins} wins" for user, wins in monthly_scores])

def format_monthly_message(session, monthly_winner, formatted_scores):
    if monthly_winner:
        winner_name = session.query(User).filter_by(id=monthly_winner.user_id).first().username
        monthly_message = session.query(MonthlyMessage).order_by(func.random()).first().message

        if "[Winner]" in monthly_message:
            monthly_message = monthly_message.replace("[Winner]", winner_name)
        
        return f"{monthly_message}\n\nScores:\n{formatted_scores}"
    else:
        return "No monthly winner found for the last month."

def send_groupme_message(message):
    url = 'https://api.groupme.com/v3/bots/post'
    data = {
        "bot_id": os.getenv('GROUPME_BOT_ID'),
        "text": message
    }
    response = requests.post(url, json=data)
    if response.status_code == 202:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message: {response.status_code}")
        print(response.json())


def send_groupme_monthly_message(session):
    last_month, current_year = get_last_month_and_year()
    monthly_winner = get_monthly_winner(session, last_month, current_year)
    formatted_scores = get_monthly_scores(session, last_month, current_year)
    message = format_monthly_message(session, monthly_winner, formatted_scores)
    send_groupme_message(message)


def send_groupme_yearly_message(session):
    # Get the current year
    current_year = datetime.now().year

    # Query the MonthlyWinner table for the winner with the most wins in the current year
    yearly_winner = session.query(MonthlyWinner.user_id, func.count(MonthlyWinner.id).label('win_count')) \
        .filter(func.extract('year', MonthlyWinner.month) == current_year) \
        .group_by(MonthlyWinner.user_id) \
        .order_by(func.count(MonthlyWinner.id).desc()) \
        .first()

    if yearly_winner:
        # Get the winner's username
        winnerName = session.query(User).filter_by(id=yearly_winner.user_id).first().username

        # Pick a random yearly message from the DB
        yearly_message = session.query(YearlyMessage).order_by(func.random()).first().message

        # Replace [Winner] with the winner's name
        if "[Winner]" in yearly_message:
            yearly_message = yearly_message.replace("[Winner]", winnerName)

        # GroupMe API endpoint
        url = 'https://api.groupme.com/v3/bots/post'

        # Payload for the API request
        data = {
            "bot_id": bot_id,
            "text": yearly_message
        }

        # Send the request to the GroupMe API
        response = requests.post(url, json=data)

        if response.status_code == 202:
            print("Message sent successfully.")
        else:
            print(f"Failed to send message: {response.status_code}")
            print(response.json())
    else:
        print("No yearly winner found.")
