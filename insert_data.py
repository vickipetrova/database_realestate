from db.models import AgentMonthlyCommission, Agent, agent_to_office, Buyer, CommissionRate, House, Seller, Listing, Sale, Office
from db.generate_data import generate_agent, generate_office, generate_seller, generate_house, generate_buyer
import uuid
import datetime
from create import engine, Session


session = Session()

# insert initial data for office, real estate agent, listings and buyers information
offices = generate_office(5)
agents = generate_agent(5)
sellers = generate_seller(5)
houses = generate_house(5)

listing_id1 = str(uuid.uuid4())
listing_id2 = str(uuid.uuid4())
listing_id3 = str(uuid.uuid4())
listing_id4 = str(uuid.uuid4())
listing_id5 = str(uuid.uuid4())
listing_ids = []
listings = []

for i in range(5):
    listing_id =  str(uuid.uuid4())
    listing_ids.append(listing_id)

    listing = Listing(listing_id = listing_id, agent_id = agents[0].agent_id, house_id = houses[i].house_id, office_id = offices[i].office_id, 
            seller_id = sellers[i].seller_id, price = 1, list_date = datetime.date(2022, 12, 1), status = "LISTED")

    listings.append(listing)

buyers = generate_buyer(5)

session.add_all(offices)
session.add_all(agents)
session.add_all(sellers)
session.add_all(houses)
session.add_all(buyers)
session.add_all(listings)
session.commit()

print("PRINTING DATABASE TABLES")
print("👱‍♂️ Agents 👱‍♂️")
print(session.query(Agent).all())
print("🏢 Offices 🏢")
print(session.query(Office).all())
print("🗒 Association table 🗒")
print(session.query(agent_to_office).all())
print("🧍‍♂️ Sellers 🧍‍♂️")
print(session.query(Seller).all())
print("🏡 Houses 🏡")
print(session.query(House).all())
print("💵 Buyers 💵")
print(session.query(Buyer).all())


print("👱‍♂️ Sellers associated with listings table before any sales:")
print(session.query(Seller).all())

def add_sale(session, buyer_id, listing_id, price, sale_date):
    try:
        # Add sale. 
        sale = Sale(sale_id = str(uuid.uuid4()), buyer_id=buyer_id, listing_id=listing_id, price=price, sale_date = sale_date)
        session.add(sale)
        # Update listing status to sold. 
        sale_listing = session.query(Listing).get(listing_id)
        print("This is the sale listing",sale_listing)
        sale_listing.status = "SOLD"
        buyer = session.query(Buyer).get(buyer_id)
        print("Buyer sales updated",buyer.sales)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        print("✅ Completed a sale with listing id = {}".format(listing_id))
        # session.close()

for i in range(3):
    add_sale(session = session, buyer_id = buyers[1].buyer_id,listing_id=listings[i].listing_id, price = 10000, sale_date=datetime.date(2022,12,3))


print("⚖️ Listings after the sale⚖️")
query = session.query(Listing).all()
for s in query:
    print(s)
print("🚀 Sales 🚀")
query = session.query(Sale).all()
for s in query:
    print(s)

session.close()
