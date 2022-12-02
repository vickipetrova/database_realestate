import random
import string
from db.models import Agent, Office, House, Seller, Buyer, Listing
import uuid
import datetime

def generate_agent(n):
    """A function used to generate n random instances of an agent for the Agent table."""
    agents = []
    for i in range(n):
        agent_id = str(uuid.uuid4())
        first_name = ''.join(random.choice(string.ascii_uppercase) for i in range(random.randint(1, 12)))
        last_name = ''.join(random.choice(string.ascii_uppercase) for i in range(random.randint(1, 12)))
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
    offices = []
    for i in range(n):
        office_id = str(uuid.uuid4())
        name = ''.join(random.choice(string.ascii_uppercase) for i in range(random.randint(1, 20)))
        zipcode = int(''.join(random.choice("0123456789") for i in range(5)))

        office = Office(office_id = str(office_id),
                  name=name,
                  zipcode=zipcode)
        offices.append(office)

    return offices

def generate_house(n):
    """A function used to generate n random instances of a house for the House table."""
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
    sellers = []
    for i in range(n):
        seller_id = str(uuid.uuid4())
        first_name = ''.join(random.choice(string.ascii_uppercase) for i in range(random.randint(1, 12)))
        last_name = ''.join(random.choice(string.ascii_uppercase) for i in range(random.randint(1, 12)))
        email = first_name + last_name + random.choice(["@gmail.com", "@yahoo.com", "@minerva.edu", "@agency.com", "outlook.com" ])
        phone = '+'.join(random.choice("0123456789") for _ in range(10))
        
        seller = Seller(seller_id = str(seller_id),
                  first_name=first_name,
                  last_name=last_name,
                  phone_number=phone,
                  email_address=email)
        sellers.append(seller)

    return sellers

def generate_buyer(n):
    """A function used to generate n random instances of a buyer for the Buyer table."""
    buyers = []
    for i in range(n):
        buyer_id = str(uuid.uuid4())
        first_name = ''.join(random.choice(string.ascii_uppercase) for i in range(random.randint(1, 12)))
        last_name = ''.join(random.choice(string.ascii_uppercase) for i in range(random.randint(1, 12)))
        email = first_name + last_name + random.choice(["@gmail.com", "@yahoo.com", "@minerva.edu", "@agency.com", "outlook.com" ])
        phone = '+'.join(random.choice("0123456789") for _ in range(10))
        
        buyer = Buyer(buyer_id = str(buyer_id),
                  first_name=first_name,
                  last_name=last_name,
                  phone_number=phone,
                  email_address=email)
        buyers.append(buyer)

    return buyers

def generate_listing(n, agent_ids, office_ids, seller_ids, house_ids):
    """A function used to generate n random instances of a listing for the Listing table."""
    listings = []
    for i in range(n):
        listing_id = str(uuid.uuid4())
        price = random.randint(10_000, 100_000_000)
        list_date = datetime.date(random.randint(2000, 2022), random.randint(1,12), random.randint(1,28))

        first_name = ''.join(random.choice(string.ascii_uppercase) for i in range(random.randint(1, 12)))
        last_name = ''.join(random.choice(string.ascii_uppercase) for i in range(random.randint(1, 12)))
        email = first_name + last_name + random.choice(["@gmail.com", "@yahoo.com", "@minerva.edu", "@agency.com", "outlook.com" ])
        phone = '+'.join(random.choice("0123456789") for _ in range(10))
        
        listing = Listing(listing_id = listing_id,
                  office_id=office_ids[i][0],
                  seller_id=seller_ids[i][0],
                  house_id=house_ids[i][0],
                  price = price,
                  list_date = list_date,
                  status = "LISTED")
        listings.append(listing)

    return listings

def generate_sale(n, agent_ids, office_ids, seller_ids, house_ids):
    """A function used to generate n random instances of a listing for the Listing table."""
    listings = []
    for i in range(n):
        listing_id = str(uuid.uuid4())
        price = random.randint(10_000, 100_000_000)
        list_date = datetime.date(random.randint(2000, 2022), random.randint(1,12), random.randint(1,28))

        first_name = ''.join(random.choice(string.ascii_uppercase) for i in range(random.randint(1, 12)))
        last_name = ''.join(random.choice(string.ascii_uppercase) for i in range(random.randint(1, 12)))
        email = first_name + last_name + random.choice(["@gmail.com", "@yahoo.com", "@minerva.edu", "@agency.com", "outlook.com" ])
        phone = '+'.join(random.choice("0123456789") for _ in range(10))
        
        listing = Listing(listing_id = listing_id,
                  office_id=office_ids[i][0],
                  seller_id=seller_ids[i][0],
                  house_id=house_ids[i][0],
                  price = price,
                  list_date = list_date,
                  status = "LISTED")
        listings.append(listing)

    return listings