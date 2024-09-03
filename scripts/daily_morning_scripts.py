import sys
import os
# Add the parent directory to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Session

from cron.cron_utils import check_for_birthday_messages, check_for_multiplier_messages

session = Session()

check_for_birthday_messages(session)
check_for_multiplier_messages(session)

session.close()
