from config import Session, headers

from cron.tasks import fetch_users_and_scores
from utils.groupme import send_groupme_daily_message

session = Session()

fetch_users_and_scores(session, headers)
send_groupme_daily_message(session)

session.close()
