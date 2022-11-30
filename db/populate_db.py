from db.models import AgenMonthlyCommission, Agent, AgentToOffice, Buyer, CommissionRate, House, Seller, Listing, Sale, Office
import uuid


def add_agent(session, first_name, last_name, phone_number, email_address, office_id = None):
    """A function to add a new record of an agent in the Agent table of the database."""
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


def add_office(session, name, zipcode, agent_id = None):
    """A function to add a new record of an Office in the Office table of the database."""
    office_id = uuid.uuid4()
    office = Office(office_id = str(office_id), 
                    name = name, 
                    zipcode = zipcode)
    session.add(office)

    # Add relation to an agent if it exists. 
    if agent_id is not None:
        agent_to_office = AgentToOffice(agent_id = str(agent_id),
                                        office_id = str(office_id))
        session.add(agent_to_office)

    session.commit()
    print ("New office created with name {}".format(name))
    if agent_id is not None:
        print("The agent was added to office {}".format(str(office_id)))

    # return office_id #DELETE? 

def add_agent_to_office_relation(session, agent_id, office_id):
    """A function to add a new record of an Office in the Agent table of the database."""
    add_agent_to_office = AgentToOffice(office_id = str(office_id), agent_id = agent_id, )
    session.add(add_agent_to_office)
    session.commit()
    print ("New office to agent relation was created between agent with id {0} and office with id {1}".format(agent_id, office_id))


def add_commission(session, commission_rate, price_lower_bound, price_upper_bound):
    """A function to add a new record of a commission in the CommissionRate table of the database."""
    row_id = uuid.uuid4()
    commission_rate = CommissionRate(id = str(row_id), 
                    price_min = price_lower_bound, 
                    price_max = price_upper_bound,
                    rate = commission_rate)
    session.add(commission_rate)
    session.commit()
    print ("New commission rate of {2} in the range {0} to {1} was created".format(price_lower_bound, price_upper_bound, commission_rate))


def add_buyer(session, first_name, last_name, email_address, phone_number):
    """A function to add a new record of a commission in the commission rate table of the database."""
    buyer_id = uuid.uuid4()
    buyer = Buyer(buyer_id = str(buyer_id), 
                    first_name = first_name, 
                    last_name = last_name,
                    email_address = email_address,
                    phone_number = phone_number)
    session.add(buyer)
    session.commit()
    print ("New buyer with name {0} {1}, email address {2}, and phone number {3} was created".format(first_name, last_name, email_address, phone_number))

