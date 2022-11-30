from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker

from db.populate_db import add_agent, add_office, add_commission, add_buyer, add_agent_to_office_relation
from db.models import Agent, Base, Office, AgentToOffice, CommissionRate, Buyer
import db.db as db

import uuid

def main():
    # Set up the DB
    engine = create_engine('sqlite:///:memory:')
    engine.connect()

    session = db.init_db(engine)

    # add_commission(session, 10, 100_000, 200_000)
    # print(session.query(CommissionRate).all())
    # add_buyer (session, "Tino", "Penchev", None, "00923840837")
    # print(session.query(Buyer).all())

    add_agent_to_office_relation(session, str(uuid.uuid4()), str(uuid.uuid4()))
    print(session.query(AgentToOffice).all())
    print(session.query(Agent).all())

    # office_id = add_office(session, 'Apple', 94102)
    # add_agent(session, "Vicki", 'Petrova', '0', 'v@email.com', office_id)

    # print(session.query(Agent).all())
    # print(session.query(Office).all())

                
if __name__ == '__main__':
    main()