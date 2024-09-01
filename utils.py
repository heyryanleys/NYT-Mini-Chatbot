import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
from dotenv import load_dotenv
import os
import re
import json
from datetime import datetime
from models import User, Score

load_dotenv()

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

