from flaskr_app.models.models import AgentMonthlyCommission, Agent, agent_to_office, Buyer, House, Seller, Listing, Sale, Office
from db_data.generate_data import generate_agent, generate_office, generate_seller, generate_house, generate_buyer, generate_listing, generate_sale
from flaskr_app import app, db


# From the documentation here it looks like the db.session automatically begins the transactions and session.begin() is outdated
# https://docs.sqlalchemy.org/en/20/orm/session_transaction.html
# https://stackoverflow.com/questions/19904176/transactions-and-sqlalchemy
# So I assumed that to be the case when writing the queries.

# Insert data for offices, agents, listings and buyers.
agents = generate_agent(25)
with app.app_context():
    db.session.add_all(agents)
    db.session.commit()

offices = generate_office(6)
sellers = generate_seller(50)
houses = generate_house(50)
buyers = generate_buyer(50)
with app.app_context():
    db.session.add_all(offices)
    db.session.add_all(sellers)
    db.session.add_all(houses)
    db.session.add_all(buyers)
    db.session.commit()

listings = generate_listing()
with app.app_context():
    # Add listings. 
    db.session.add_all(listings)
    # If the agent isn't associated with the office of the listing, add that the agent worked for the office since they're both on the listing. 
    for listing in listings:
        related_agent = Agent.query.get(listing.agent_id)
        related_office = Office.query.get(listing.office_id)
        if related_office not in related_agent.offices:
            related_agent.offices.append(related_office)
            db.session.add(related_office)
    # Commit only after all relevant changes were made. 
    db.session.commit()

    print("\n PRINTING DATABASE TABLES -- to see that the items loaded successfully in the DB\n")
    print("\n 👱‍♂️ Agents 👱‍♂️\n ")

    print(db.session.query(Agent).all())
    print("\n 🏢 Offices 🏢\n ")
    print(db.session.query(Office).all())
    print("\n 🗒 Association table Agent-Office 🗒\n ")
    print(db.session.query(agent_to_office).all())
    print("\n 🧍‍♂️ Sellers 🧍‍♂️\n ")
    print(db.session.query(Seller).all())
    print("\n 🏡 Houses 🏡\n")
    print(db.session.query(House).all())
    print("\n 💵 Buyers 💵 \n ")
    print(db.session.query(Buyer).all())


    print("\n 👱‍♂️ Sellers associated with listings table before any sales:\n")
    print(db.session.query(Listing).all())

sales = generate_sale()

with app.app_context():
    db.session.add_all(sales)
    for sale in sales:
        related_listing = Listing.query.get(sale.listing_id)
        related_listing.status = "SOLD"
        db.session.add(related_listing)
    db.session.commit()

    print("\n Listings after the sale 🌈 \n ")
    query = db.session.query(Listing).all()
    for s in query:
        print(s)
    print("\n 🚀 Sales 🚀\n ")
    query = db.session.query(Sale).all()
    for s in query:
        print(s)
