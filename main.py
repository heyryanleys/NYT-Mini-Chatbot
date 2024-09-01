from config import Session, headers
from tasks import fetch_users_and_scores
from tasks import schedule_tasks
from utils import send_groupme_daily_message, send_groupme_monthly_message


# Database session
session = Session()

# For testing, manually call fetch users and scores
fetch_users_and_scores(session, headers)
send_groupme_monthly_message(session)

#Schedule tasks to run daily
# schedule_tasks(session, headers)

session.close()
