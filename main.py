from config import Session, headers
from tasks import fetch_users_and_scores
from tasks import schedule_tasks


# Database session
session = Session()

# For testing, manually call fetch users and scores
fetch_users_and_scores(session, headers)

#Schedule tasks to run daily
schedule_tasks(session, headers)



session.close()
