from utils.nyt import get_daily_scores, get_leaderboard_users
from cron.cron_utils import check_for_birthday, get_multipliers_by_date
from utils.database import save_users_to_db, save_scores_to_db, save_multiplier_to_score
from models import DailyMultiplier, User, Score
from sqlalchemy.sql import extract
import random
from datetime import datetime, timedelta

def fetch_users_and_scores(session, headers):
    """Fetches users and scores and saves them to the database, applying multipliers as necessary."""
    print("Fetching and saving new users...")
    users_data = get_leaderboard_users(headers)
    if users_data:
        save_users_to_db(session, users_data)

    print("Fetching and saving today's crossword scores...")
    scores_data = get_daily_scores(headers)
    if scores_data:
        save_scores_to_db(session, scores_data)
        apply_multiplier(session)

def apply_multiplier(session):
    """Applies the appropriate multiplier based on priority: Birthday > Daily Double."""
    print("Checking for multipliers...")

    # Todays' scores
    todays_scores = session.query(Score).filter_by(date=datetime.now().date()).all()

    # Get tomorrow's scores from the DB
    # tomorrows_scores = session.query(Score).filter_by(date=datetime.now().date() + timedelta(days=1)).all()

    # Get today's multipliers
    todays_multipliers = get_multipliers_by_date(session)

    if todays_multipliers:
        # Create a dictionary of multipliers keyed by user_id
        multiplier_dict = {multiplier.user_id: multiplier.multiplier for multiplier in todays_multipliers if multiplier.user_id is not None}
        # Default multiplier for general multipliers (where user_id is None)
        general_multiplier = next((multiplier.multiplier for multiplier in todays_multipliers if multiplier.user_id is None), None)

        for score in todays_scores:
            # Apply the user-specific multiplier or general multiplier
            user_multiplier = multiplier_dict.get(score.user_id, general_multiplier)
            if user_multiplier:
                save_multiplier_to_score(session, score.user_id, multiplier=user_multiplier)

        # Update score records where rank is 1
        for score in todays_scores:
            if score.rank == 1:
                score.points = score.rank * score.multiplier

    else: 
        # Make score 1 because no multiplier
        for score in todays_scores:
            if score.rank == 1:
                score.points = 1
        

    session.commit()

def has_multiplier_for_today(session, date):
    """Checks if a multiplier already exists for the given date."""
    return session.query(DailyMultiplier).filter_by(date=date).first()
                

def create_daily_double_multiplier(session):
    """Picks a random day in the month to be the Daily Double day, trying up to 10 times."""
    
    attempts = 0
    while attempts < 10:
        random_day = random.randint(1, 28)  # To avoid issues with February
        double_day = datetime.now().replace(day=random_day)
        # double_day = datetime.now().replace(day=1) # for testing
        
        if not has_multiplier_for_today(session, date=double_day):
            # Save the Daily Double day to the database
            daily_double = DailyMultiplier(date=double_day, multiplier=2, multiplier_type='Daily Double')
            session.add(daily_double)
            session.commit()
            return
        attempts += 1

def create_birthday_multipliers(session):
    """Creates multipliers for users' birthdays."""
    users = session.query(User).filter(extract('month', User.birthday) == datetime.now().month).all()
    print(users)
    for user in users:
        birthday_multiplier = DailyMultiplier(date=user.birthday, multiplier=3, multiplier_type='Birthday', user_id=user.id)
        session.add(birthday_multiplier)
        session.commit()