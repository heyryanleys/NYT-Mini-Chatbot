from config import Session, headers
from cron.scheduler import schedule_tasks
from cron.tasks import fetch_users_and_scores
from utils.groupme import send_groupme_daily_message, send_groupme_monthly_message, send_groupme_yearly_message

# Database session
session = Session()

# For testing, manually call fetch users and scores
fetch_users_and_scores(session, headers)
# send_groupme_daily_message(session)
# check_for_birthday_messages(session)




# Schedule tasks to run daily
# schedule_tasks(session, headers)

session.close()
