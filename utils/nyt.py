import requests
from bs4 import BeautifulSoup
import re
import json

def get_leaderboard_users(headers):
    url = "https://www.nytimes.com/svc/crosswords/v6/leaderboard/mini.json"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def get_daily_scores(headers):
    url = "https://www.nytimes.com/puzzles/leaderboards"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find('script', string=re.compile('window.data'))
    if script:
        json_data = re.search(r'window\.data\s*=\s*(\{.*\});?', script.string, re.DOTALL)
        if json_data:
            return json.loads(json_data.group(1))
    return None