from config import Session

from cron.tasks import create_daily_double_multiplier, create_birthday_multipliers

session = Session()

create_birthday_multipliers(session)
create_daily_double_multiplier(session)

session.close()
