from sqlalchemy.orm import sessionmaker
from db.models import Base

def init_db(engine):
    """A function to initialize the tables of the databse and create the session."""
    # Delete tables
    Base.metadata.drop_all(bind=engine)   
    # Create tables
    Base.metadata.create_all(bind=engine)   

    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()

    return session



