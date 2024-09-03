from config import Session

from utils.groupme import send_groupme_yearly_message

session = Session()

send_groupme_yearly_message(session)

session.close()
