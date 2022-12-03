import random
import string
from flaskr_app.models.models import Agent, Office, House, Seller, Buyer, Listing, Sale
from flaskr_app import app, db
import uuid
import datetime
import random

from faker import Faker
fake = Faker()


def generate_agent(n):
    """A function used to generate n random instances of an agent for the Agent table."""

    print("🔄 Generating agents ... ")
    agents = []
    for i in range(n):
        agent_id = str(uuid.uuid4())
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = first_name + last_name + random.choice(["@gmail.com", "@yahoo.com", "@minerva.edu", "@agency.com", "outlook.com" ])
        phone = '+'+''.join(random.choice("0123456789") for _ in range(10))

        agent = Agent(agent_id = str(agent_id),
                  first_name=first_name,
                  last_name=last_name,
                  phone_number=phone,
                  email_address=email)
        agents.append(agent)

    return agents

def generate_office(n):
    """A function used to generate n random instances of an office for the Office table."""

    with app.app_context():
        agents = Agent.query.all()

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

def generate_house(n):
    """A function used to generate n random instances of a house for the House table."""

    print("🔄 Generating houses ... ")

    houses = []
    for i in range(n):
        house_id = str(uuid.uuid4())
        bedrooms_num = ''.join(random.choice(string.ascii_uppercase) for i in range(random.randint(1, 20)))
        bathrooms_num = int(''.join(random.choice("0123456789") for i in range(5)))
        zipcode = int(''.join(random.choice("0123456789") for i in range(5)))

        house = House(house_id = str(house_id),
                  bedrooms_num=bedrooms_num,
                  bathrooms_num = bathrooms_num,
                  zipcode=zipcode)
        houses.append(house)

    return houses

def generate_seller(n):
    """A function used to generate n random instances of a seller for the Seller table."""

    print("🔄 Generating sellers ... ")

    sellers = []
    for i in range(n):
        seller_id = str(uuid.uuid4())
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = first_name + last_name + random.choice(["@gmail.com", "@yahoo.com", "@minerva.edu", "@agency.com", "outlook.com" ])
        phone = '+'+''.join(random.choice("0123456789") for _ in range(10))
        
        seller = Seller(seller_id = str(seller_id),
                  first_name=first_name,
                  last_name=last_name,
                  phone_number=phone,
                  email_address=email)
        sellers.append(seller)

    return sellers

def generate_buyer(n):
    """A function used to generate n random instances of a buyer for the Buyer table."""

    print("🔄 Generating buyers ... ")

    buyers = []
    for i in range(n):
        buyer_id = str(uuid.uuid4())
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = first_name + last_name + random.choice(["@gmail.com", "@yahoo.com", "@minerva.edu", "@agency.com", "@outlook.com" ])
        phone = '+'+''.join(random.choice("0123456789") for _ in range(10))
        
        buyer = Buyer(buyer_id = str(buyer_id),
                  first_name=first_name,
                  last_name=last_name,
                  phone_number=phone,
                  email_address=email)
        buyers.append(buyer)

    return buyers

def generate_listing():
    """A function used to generate n random instances of a listing for the Listing table."""
    with app.app_context():
        agents = Agent.query.all()
        houses = House.query.all()
        sellers = Seller.query.all()
        offices = Office.query.all()

    n = len(houses)
    sample_houses = random.sample(houses, n)
    sample_agents = random.choices(agents, k=n)
    sample_sellers = random.choices(sellers, k=n)
    sample_offices = random.choices(offices, k=n)

    print("🔄 Generating listings ... ")


    listings = []
    for i in range(n):
        listing_id = str(uuid.uuid4())
        price = random.randint(10_000, 100_000_000)
        list_date = datetime.date(random.randint(2019, 2022), random.randint(1,12), random.randint(1,28))

        listing = Listing(listing_id = listing_id,
                  agent_id = sample_agents[i].agent_id,
                  office_id=sample_offices[i].office_id,
                  seller_id=sample_sellers[i].seller_id,
                  house_id=sample_houses[i].house_id,
                  price = price,
                  list_date = list_date,
                  status = "LISTED")
        listings.append(listing)

    return listings

def generate_sale():
    """A function used to generate n random instances of a listing for the Listing table."""

    with app.app_context():
        listings = Listing.query.all()
        buyers = Buyer.query.all()
        sellers = Seller.query.all()

    n = len(buyers)
    sample_buyers = random.sample(buyers, n)
    sample_sellers = random.sample(sellers, n)
    sample_listings = random.sample(listings, n)

    print("🔄 Generating sales ... ")

    sales = []
    for i in range(n):
        sale_id = str(uuid.uuid4())
        price = random.randint(10_000, 1_000_000)
        # sale_date = datetime.date(random.randint(sample_listings[i].list_date[:4], 2022), random.randint(sample_listings[i].list_date[4:6],12), random.randint(sample_listings[i].list_date[6:],28))
        sale_date = datetime.date(random.randint(sample_listings[i].list_date.year, 2022), random.randint(sample_listings[i].list_date.month,12), random.randint(sample_listings[i].list_date.day,28))

        sale = Sale(sale_id = sale_id,
                  listing_id=sample_listings[i].listing_id,
                  buyer_id=sample_buyers[i].buyer_id,
                  price = price,
                  sale_date = sale_date)

        sales.append(sale)

    return sales