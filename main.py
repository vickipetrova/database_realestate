from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker

from populate_db import add_agent, add_office
from models import Agent, Base, Office, AgentToOffice
import db


def main():
    # Set up the DB
    engine = create_engine('sqlite:///:memory:')
    engine.connect()

    session = db.init_db(engine)

    add_agent(session, "Kate", 'Fourie', '12323', 'kate@gmail.com')

    office_id = add_office(session, 'Apple', 94102)
    add_agent(session, "Vicki", 'Petrova', '0', 'v@email.com', office_id)

    # print(session.query(Agent).all())
    # print(session.query(Office).all())
    print(session.query(AgentToOffice).all())

                
if __name__ == '__main__':
    main()