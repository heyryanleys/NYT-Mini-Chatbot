from config import Session

from cron.cron_utils import check_for_birthday_messages, check_for_multiplier_messages

session = Session()

check_for_birthday_messages(session)
check_for_multiplier_messages(session)

session.close()
