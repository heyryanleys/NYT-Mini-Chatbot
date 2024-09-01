from apscheduler.schedulers.blocking import BlockingScheduler
from utils import get_daily_scores, save_scores_to_db, get_leaderboard_users, save_users_to_db, send_groupme_daily_message, send_groupme_monthly_message, send_groupme_yearly_message

def fetch_users_and_scores(session, headers):
    # Fetch and save new users first
    print("Fetching and saving new users...")
    users_data = get_leaderboard_users(headers)
    if users_data:
        save_users_to_db(session, users_data)

    # Then fetch and save scores
    print("Fetching and saving today's crossword scores...")
    scores_data = get_daily_scores(headers)
    if scores_data:
        save_scores_to_db(session, scores_data)

def send_daily_groupme_message(session):
    print("Sending daily GroupMe message...")
    send_groupme_daily_message(session)

def send_monthly_winner_message(session):
    print("Sending monthly winner message...")
    send_groupme_monthly_message(session)  # Replace with logic to determine and send monthly winner message

def send_yearly_winner_message(session):
    print("Sending yearly winner message...")
    send_groupme_yearly_message(session)  # Replace with logic to determine and send yearly winner message

def schedule_tasks(session, headers):
    scheduler = BlockingScheduler()
    
    # Schedule the combined job for fetching users and scores
    scheduler.add_job(lambda: fetch_users_and_scores(session, headers), 'cron', day_of_week='mon-sat', hour=22, minute=0, timezone='US/Eastern')
    scheduler.add_job(lambda: fetch_users_and_scores(session, headers), 'cron', day_of_week='sun', hour=18, minute=0, timezone='US/Eastern')
    
    # Schedule the daily message to be sent at 10:05 PM ET (Mon-Sat) and 6:05 PM ET (Sun)
    scheduler.add_job(lambda: send_daily_groupme_message(session), 'cron', day_of_week='mon-sat', hour=22, minute=5, timezone='US/Eastern')
    scheduler.add_job(lambda: send_daily_groupme_message(session), 'cron', day_of_week='sun', hour=18, minute=5, timezone='US/Eastern')
    
    # Schedule the monthly winner message to be sent on the 1st day of every month at 10:00 AM ET
    scheduler.add_job(lambda: send_monthly_winner_message(session), 'cron', day=1, hour=10, minute=0, timezone='US/Eastern')
    
    # Schedule the yearly winner message to be sent on the 1st day of every year at 10:00 AM ET
    scheduler.add_job(lambda: send_yearly_winner_message(session), 'cron', month=1, day=1, hour=10, minute=0, timezone='US/Eastern')

    scheduler.start()
