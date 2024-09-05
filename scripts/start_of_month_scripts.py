import sys
import os
# Add the parent directory to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Session

from cron.tasks import create_daily_double_multiplier, create_birthday_multipliers
from utils.groupme import send_groupme_monthly_message

session = Session()

send_groupme_monthly_message(session)
create_birthday_multipliers(session)
create_daily_double_multiplier(session)

session.close()
