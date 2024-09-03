from config import Session

from utils.groupme import send_groupme_monthly_message

session = Session()

send_groupme_monthly_message(session)

session.close()
