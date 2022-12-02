# Import necessary installs and imports.
from sqlalchemy.sql import func

# Non-abstract classes.
from sqlalchemy import Table, Column, Text, Integer, ForeignKey, select, update, Numeric, String, Date
from sqlalchemy.orm import relationship 

# Declarative base class.
from sqlalchemy.orm import declarative_base
Base = declarative_base()

# Assossiaction table between Agent and Office class for many-to-many relationship.
# Documentation: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
agent_to_office = Table('agent_to_office', 
    Base.metadata,
    Column('agent_id', Text(length=36), ForeignKey(
                'agents.agent_id', ondelete='CASCADE')),
    Column('office_id', Text(length=36), ForeignKey(
                'offices.office_id', ondelete='CASCADE'))
)

class Agent(Base):  # Python class name
    __tablename__='agents'  # SQL table name
    agent_id = Column(Text(length=36), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    email_address = Column(String)

    offices = relationship("Office", secondary=agent_to_office, back_populates = 'agents') #many to many - an agent can work for many offices and an office can have many agents working for it
    listings = relationship("Listing") #one to many - a listing can have one agent linked to it but an agent can have multiple listings
    commissions = relationship("AgentMonthlyCommission", back_populates = "agent") #one to many - an agent can have multiple commissions - one for each month of the year, a commission is linked to a single agent

    def __repr__(self):
        return "Agent(agent_id={0}, first_name={1}, last_name={2}, phone_number={3}, email_address={4})".format(self.agent_id, self.first_name, self.last_name, self.phone_number, self.email_address)


class Office(Base):
    __tablename__ = 'offices'
    office_id = Column(Text(length=36), primary_key=True)
    name = Column(String)
    zipcode = Column(Integer)

    agents = relationship("Agent", secondary=agent_to_office, back_populates = 'offices') #many to many - an agent can work for many offices and an office can have many agents working for it
    listings = relationship("Listing", back_populates = "office") #one to many - one office can have many listings, but a listing can be only from a single office

    def __repr__(self):
        return "Office(office_id={0}, name = {1}, zipcode={2})".format(self.office_id, self.name, self.zipcode)

class House(Base):  
    __tablename__='houses'  
    house_id = Column(Text(length=36), primary_key=True)
    bedrooms_num = Column(Integer)
    bathrooms_num = Column(Integer)
    zipcode = Column(Integer)

    listings = relationship("Listing") #one to many - a listing is linked to a single house, but a house can be linked to multiple listings - 
                                    #e.g. selling it for different prices at two different offices or by two different agents (an office in LA might sell it for more money than an office in a small town) 

    def __repr__(self):
        return "House(house_id={0}, bedrooms_num={1}, bathrooms_num={2}, zipcode={3})".format(self.house_id, self.bedrooms_num, self.bathrooms_num, self.zipcode)

class Seller(Base):  
    __tablename__='sellers'  
    seller_id = Column(Text(length=36), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email_address= Column(String)
    phone_number = Column(String)

    listings = relationship("Listing") #one to many - one seller can sell multiple listings, but a listing can be sold by a single seller 
                                #possible point for improvement e.g. what if it's a married couple selling a property, not sure how it works legally - I assume there is a single seller

    def __repr__(self):
        return "Seller(seller_id={0}, first_name={1}, last_name={2}, email_address={3}, phone_number = {4})".format(self.seller_id, self.first_name, self.last_name, self.email_address, self.phone_number)

class Buyer(Base):  
    __tablename__='buyers'  
    buyer_id = Column(Text(length=36), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email_address= Column(String)
    phone_number = Column(String)

    sales = relationship("Sale", back_populates = "buyer")#one to many - a buyer can buy many different listings (linked to multiple sales) but a sale can only be linked to a single buyer 
                    #(I assume this to be the case, not sure how it works leaglly with married couples for example)

    def __repr__(self):
        return "Buyer(buyer_id={0}, first_name={1}, last_name={2}, email_address={3}, phone_number = {4})".format(self.buyer_id, self.first_name, self.last_name, self.email_address, self.phone_number)


class Listing(Base):  
    __tablename__='listings'  
    listing_id = Column(Text(length=36), primary_key=True)
    agent_id = Column(Text(length=36), ForeignKey(
                'agents.agent_id', ondelete='CASCADE')) #one to many - a listing can have one agent linked to it but an agent can have multiple listings
    office_id = Column(Text(length=36), ForeignKey(
                'offices.office_id', ondelete='CASCADE')) #one to many - one office can have many listings, but a listing can be only from a single office
    seller_id = Column(Text(length=36), ForeignKey(
                'sellers.seller_id', ondelete='CASCADE')) #one to many - one seller can sell multiple listings, but a listing can be sold by a single seller 
                                    #possible point for improvement e.g. what if it's a married couple selling a property - I assume there is a single seller
    house_id = Column(Text(length=36), ForeignKey(
                'houses.house_id', ondelete='CASCADE')) #one to many - a listing is linked to a single house, but a house can be linked to multiple listings - 
                                    #e.g. selling it for different prices at two different offices or by two different agents (an office in LA might sell it for more money than an office in a small town)
    
    price = Column(Numeric(19,2))
    list_date = Column(Date, server_default = func.now())
    status = Column(Text, default = "LISTED")

    office = relationship("Office", back_populates = "listings")

    def __repr__(self):
        return "Listing(listing_id={0}, agent_id={1}, office_id={2}, seller_id={3}, house_id = {4}, price = {5}, list_date = {6}, status = {7})".format(self.listing_id, self.agent_id, self.office_id, self.seller_id, self.house_id, self.price, self.list_date, self.status)

class Sale(Base):  
    __tablename__='sales'  
    sale_id = Column(Text(length=36), primary_key=True)
    listing_id = Column(Text(length=36), ForeignKey(
                'listings.listing_id', ondelete='CASCADE'), 
                primary_key = True) #
    buyer_id = Column(Text(length=36), ForeignKey(
                'buyers.buyer_id', ondelete='CASCADE'))

    buyer = relationship("Buyer", back_populates="sales")

    price = Column(Numeric(19,2))
    sale_date = Column(Date, server_default = func.now())

    def __repr__(self):
        return "Sale(sale_id={0}, listing_id={1}, buyer_id={2}, price={3}, sale_date = {4})".format(self.sale_id, self.listing_id, self.buyer_id, self.price, self.sale_date)


class AgentMonthlyCommission(Base):  
    __tablename__='agentmonthlycommissions'  
    agent_id = Column(Text(length=36), ForeignKey(
                'agents.agent_id', ondelete='CASCADE'), 
                primary_key = True)
    agent = relationship("Agent", back_populates = 'commissions')
    commission_amount = Column(Numeric(19,2))
    start_date = Column(Date, server_default = func.now(), primary_key = True)
    end_date = Column(Date, server_default = func.now(), primary_key = True)

    def __repr__(self):
        return "AgentMonthlyCommission(agent_id={0}, commission_amount={1}, start_date={2}, end_date = {3})".format(self.agent_id, self.commission_amount, self.start_date, self.end_date)

# Delete this? 
class CommissionRate(Base):  
    __tablename__='commissionrates'  
    id = Column(Text(length=36), primary_key=True)
    price_min = Column(Numeric(19,2), nullable=False)
    price_max = Column(Numeric(19,2), nullable=False)
    rate = Column(Numeric(3,2), nullable=False)

    def __repr__(self):
        return "Commissionrate(price_min={0}, price_max={1}, rate={2})".format(self.price_min, self.price_max, self.rate)    