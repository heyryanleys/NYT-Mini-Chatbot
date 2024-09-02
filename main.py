from config import Session, headers
from cron.scheduler import schedule_tasks
from cron.tasks import fetch_users_and_scores
from utils.groupme import send_groupme_daily_message, send_groupme_monthly_message, send_groupme_yearly_message
from cron.cron_utils import check_for_birthday_messages, check_for_multiplier_messages
from cron.tasks import create_daily_double_multiplier, create_birthday_multipliers

# Database session
session = Session()

# For testing, manually call fetch users and scores
# create_birthday_multipliers(session)
# create_daily_double_multiplier(session)
# check_for_birthday_messages(session)
# check_for_multiplier_messages(session)
# fetch_users_and_scores(session, headers)
# send_groupme_yearly_message(session)
# send_groupme_daily_message(session)
# send_groupme_monthly_message(session)

# Schedule tasks to run daily on production
schedule_tasks(session, headers)

session.close()
