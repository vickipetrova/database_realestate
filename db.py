from sqlalchemy.orm import sessionmaker
from models import Base

def init_db(engine):
    # Delete tables
    Base.metadata.drop_all(bind=engine)   
    # Create tables
    Base.metadata.create_all(bind=engine)   

    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()

    return session