from apscheduler.schedulers.blocking import BlockingScheduler
from utils import get_daily_scores, save_scores_to_db, get_leaderboard_users, save_users_to_db

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

def schedule_tasks(session, headers):
    scheduler = BlockingScheduler()
    # Schedule the combined job for 10 PM ET on weekdays and 6 PM ET on Sundays
    scheduler.add_job(lambda: fetch_users_and_scores(session, headers), 'cron', day_of_week='mon-sat', hour=22, timezone='US/Eastern')
    scheduler.add_job(lambda: fetch_users_and_scores(session, headers), 'cron', day_of_week='sun', hour=18, timezone='US/Eastern')

    scheduler.start()
