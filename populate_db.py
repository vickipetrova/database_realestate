from models import Agent, Office, AgentToOffice
import uuid


def add_agent(session, first_name, last_name, phone_number, email_address, office_id = None):
    agent_id = uuid.uuid4()
    agent = Agent(agent_id = str(agent_id),
                  first_name=first_name,
                  last_name=last_name,
                  phone_number=phone_number,
                  email_address=email_address)

    session.add(agent)

    if office_id is not None:
        agent_to_office = AgentToOffice(agent_id = str(agent_id),
                                        office_id = str(office_id))
        session.add(agent_to_office)

    session.commit()
    print ("New agent created with first name {0} and last name {1}".format(first_name, last_name))
    if office_id is not None:
        print("The agent was added to office {}".format(str(office_id)))


def add_office(session, name, zipcode):
    office_id = uuid.uuid4()
    office = Office(office_id = str(office_id), 
                    name=name, 
                    zipcode=zipcode)
    session.add(office)
    session.commit()
    print ("New office created with name {}".format(name))
    return office_id