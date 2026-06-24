from .mongo import db
from .movies import MoviesDB
from .users import UsersDB
from .analytics import AnalyticsDB

movies_db = MoviesDB(db)
users_db = UsersDB(db)
analytics_db = AnalyticsDB(db)
