import sys
import os
# Add the parent directory to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Session

from utils.groupme import send_groupme_monthly_message

session = Session()

send_groupme_monthly_message(session)

session.close()
