from flaskr_app.models.models import AgentMonthlyCommission, Agent, Buyer, House, Seller, Listing, Sale, Office
from db_data.generate_data import generate_agent, generate_seller, generate_house, generate_buyer
import uuid
import datetime
import random
import string


def test_data(db):

    agents = generate_agent(5)
    db.session.add_all(agents)
    db.session.commit()

    offices = generate_office(5, agents=agents)
    sellers = generate_seller(5)
    houses = generate_house(5)


    listing_ids = []
    listings = []
    for i in range(5):
        listing_id =  str(uuid.uuid4())
        listing_ids.append(listing_id)

        listing = Listing(listing_id = listing_id, agent_id = agents[0].agent_id, house_id = houses[i].house_id, office_id = offices[i].office_id, 
                seller_id = sellers[i].seller_id, price = 1000, list_date = datetime.date(2022, 12, 1), status = "LISTED")

        listings.append(listing)

    buyers = generate_buyer(5)

    db.session.add_all(offices)
    db.session.add_all(agents)
    db.session.add_all(sellers)
    db.session.add_all(houses)
    db.session.add_all(buyers)
    db.session.add_all(listings)
    db.session.commit()

    print("PRINTING DATABASE TABLES")
    print("👱‍♂️ Agents 👱‍♂️")
    print(db.session.query(Agent).all())
    print("🏢 Offices 🏢")
    print(db.session.query(Office).all())
    print("🗒 Association table 🗒")
    print("🧍‍♂️ Sellers 🧍‍♂️")
    print(db.session.query(Seller).all())
    print("🏡 Houses 🏡")
    print(db.session.query(House).all())
    print("💵 Buyers 💵")
    print(db.session.query(Buyer).all())


    print("👱‍♂️ Sellers associated with listings table before any sales:")
    print(db.session.query(Seller).all())

    def add_sale(session, buyer_id, listing_id, price, sale_date):
        try:
            # Add sale. 
            sale = Sale(sale_id = str(uuid.uuid4()), buyer_id=buyer_id, listing_id=listing_id, price=price, sale_date = sale_date)
            session.add(sale)
            # Update listing status to sold. 
            sale_listing = session.query(Listing).get(listing_id)
            sale_listing.status = "SOLD"
            buyer = session.query(Buyer).get(buyer_id)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            print("✅ Completed a sale with listing id = {}".format(listing_id))

    for i in range(3):
        add_sale(session = db.session, buyer_id = buyers[1].buyer_id,listing_id=listings[i].listing_id, price = 10000, sale_date=datetime.date(2022,12,3))


    print("⚖️ Listings after the sale⚖️")
    query = db.session.query(Listing).all()
    for s in query:
        print(s)
    print("🚀 Sales 🚀")
    query = db.session.query(Sale).all()
    for s in query:
        print(s)


def generate_office(n, agents):
    """A function used to generate n random instances of an office for the Office table."""

    sample_agents = random.choices(agents, k=n)

    print("🔄 Generating offices ... ")

    offices = []
    for i in range(n):
        office_id = str(uuid.uuid4())
        name = ''.join(random.choice(string.ascii_uppercase) for i in range(random.randint(1, 20)))
        zipcode = int(''.join(random.choice("0123456789") for i in range(5)))

        office = Office(office_id = str(office_id),
                  name=name,
                  zipcode=zipcode)

        office.agents.append(sample_agents[i])

        offices.append(office)

    return offices