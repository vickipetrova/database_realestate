from sqlalchemy import create_engine, MetaData
from db.models import Base

# Set up the DB.
# Initiate engine and creating a file for the db. 
engine = create_engine('sqlite:///data.db', echo = False)
engine.connect()

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

from sqlalchemy.orm import sessionmaker
# Create session
Session = sessionmaker(bind=engine)
