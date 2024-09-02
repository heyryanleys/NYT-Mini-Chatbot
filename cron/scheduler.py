from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from utils.groupme import send_groupme_daily_message, send_groupme_monthly_message, send_groupme_yearly_message, send_groupme_daily_double_message
from cron.cron_utils import get_last_day_of_month, get_last_day_of_year, check_for_birthday_messages, check_for_multiplier_messages
from cron.tasks import fetch_users_and_scores, create_daily_double_multiplier, create_birthday_multipliers
    
def schedule_tasks(session, headers):
    scheduler = BlockingScheduler()

    # Schedule the Daily Double for each month
    schedule_multipliers(scheduler, session)

    # Schedule daily tasks
    schedule_daily_tasks(scheduler, session, headers)

    # Schedule monthly and yearly tasks
    schedule_monthly_and_yearly_tasks(scheduler, session)

    scheduler.start()

def schedule_multipliers(scheduler, session):
    """Schedules the Daily Double day, with a random day each month."""
    scheduler.add_job(lambda: create_birthday_multipliers(session), 'cron', day=1, hour=0, minute=0, timezone='US/Eastern')
    scheduler.add_job(lambda: create_daily_double_multiplier(session), 'cron', day='1', hour=0, minute=0, timezone='US/Eastern')

def schedule_daily_tasks(scheduler, session, headers):
    scheduler.add_job(lambda: check_for_birthday_messages(session), 'cron', day_of_week='mon-sun', hour=9, minute=0, timezone='US/Eastern')
    scheduler.add_job(lambda: check_for_multiplier_messages(session), 'cron', day_of_week='mon-sun', hour=9, minute=0, timezone='US/Eastern')

    # Fetch users and scores at 10 PM (Mon-Sat) or 6 PM (Sun)
    scheduler.add_job(lambda: fetch_users_and_scores(session, headers), 'cron', day_of_week='mon-sat', hour=22, minute=0, timezone='US/Eastern')
    scheduler.add_job(lambda: fetch_users_and_scores(session, headers), 'cron', day_of_week='sun', hour=18, minute=0, timezone='US/Eastern')

    # Send daily summary at 10:02 PM (Mon-Sat) or 6:02 PM (Sun)
    scheduler.add_job(lambda: send_groupme_daily_message(session), 'cron', day_of_week='mon-sat', hour=22, minute=2, timezone='US/Eastern')
    scheduler.add_job(lambda: send_groupme_daily_message(session), 'cron', day_of_week='sun', hour=18, minute=2, timezone='US/Eastern')

def schedule_monthly_and_yearly_tasks(scheduler, session):
    for month in range(1, 13):
        last_day = get_last_day_of_month(datetime.now().year, month)
        if last_day.weekday() == 6:  # Sunday
            scheduler.add_job(lambda: send_groupme_monthly_message(session), 'date', run_date=last_day.replace(hour=18, minute=2), timezone='US/Eastern')
        else:
            scheduler.add_job(lambda: send_groupme_monthly_message(session), 'date', run_date=last_day.replace(hour=22, minute=2), timezone='US/Eastern')
    
    last_day_of_year = get_last_day_of_year(datetime.now().year)
    if last_day_of_year.weekday() == 6:  # Sunday
        scheduler.add_job(lambda: send_groupme_yearly_message(session), 'date', run_date=last_day_of_year.replace(hour=18, minute=2), timezone='US/Eastern')
    else:
        scheduler.add_job(lambda: send_groupme_yearly_message(session), 'date', run_date=last_day_of_year.replace(hour=22, minute=2), timezone='US/Eastern')


