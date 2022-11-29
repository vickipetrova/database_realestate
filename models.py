# Import necessary installs and imports.
import sqlalchemy
from sqlalchemy.sql import func

# Non-abstract classes.
from sqlalchemy import Table, Column, Text, Integer, ForeignKey, DateTime, select, update, Numeric, String, Date

from sqlalchemy.orm import relationship, session, sessionmaker

from sqlalchemy.dialects.postgresql import UUID

# Declarative base class.
from sqlalchemy.orm import declarative_base
Base = declarative_base()


class Agent(Base):  # Python class name
    __tablename__='agents'  # SQL table name
    agent_id = Column(Text(length=36), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    email_address = Column(String)

    def __repr__(self):
        return "Agent(agent_id={0}, first_name={1}, last_name={2}, phone_number={3}, email_address={4})".format(self.agent_id, self.first_name, self.last_name, self.phone_number, self.email_address)


class Office(Base):
    __tablename__ = 'offices'
    office_id = Column(Text(length=36), primary_key=True)
    name = Column(String)
    zipcode = Column(Integer)

    def __repr__(self):
        return "Office(office_id={0}, name = {1}, zipcode={2})".format(self.office_id, self.name, self.zipcode)


class AgentToOffice(Base):
    __tablename__ = 'agent_to_office'
    
    agent_id = Column(Text(length=36), ForeignKey(
                'agents.agent_id', ondelete='CASCADE'), 
                primary_key = True)
    office_id = Column(Text(length=36), ForeignKey(
                'offices.office_id', ondelete='CASCADE'), 
                primary_key = True)

    # office = relationship('Office', backref='agents')  # Need to google this

    def __repr__(self):
        return "AgentToOffice(agent_id={0}, office_id = {1})".format(self.agent_id, self.office_id)


class House(Base):  
    __tablename__='houses'  
    house_id = Column(Text(length=36), primary_key=True)
    bedrooms_num = Column(Integer)
    bathrooms_num = Column(Integer)
    zipcode = Column(Integer)

    def __repr__(self):
        return "House(house_id={0}, bedrooms_num={1}, bathrooms_num={2}, zipcode={3})".format(self.house_id, self.bedrooms_num, self.bathrooms_num, self.zipcode)

class Seller(Base):  
    __tablename__='sellers'  
    seller_id = Column(Text(length=36), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email_address= Column(String)
    phone_number = Column(String)

    def __repr__(self):
        return "Seller(seller_id={0}, first_name={1}, last_name={2}, email_address={3}, phone_number = {4})".format(self.seller_id, self.first_name, self.last_name, self.email_address, self.phone_number)

class Buyer(Base):  
    __tablename__='buyers'  
    buyer_id = Column(Text(length=36), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email_address= Column(String)
    phone_number = Column(String)

    def __repr__(self):
        return "Buyer(buyer_id={0}, first_name={1}, last_name={2}, email_address={3}, phone_number = {4})".format(self.buyer_id, self.first_name, self.last_name, self.email_address, self.phone_number)


class Listing(Base):  
    __tablename__='listings'  
    listing_id = Column(Text(length=36), primary_key=True)
    agent_id = Column(Text(length=36), ForeignKey(
                'agents.agent_id', ondelete='CASCADE'), 
                primary_key = True)
    office_id = Column(Text(length=36), ForeignKey(
                'offices.office_id', ondelete='CASCADE'), 
                primary_key = True)
    seller_id = Column(Text(length=36), ForeignKey(
                'sellers.seller_id', ondelete='CASCADE'), 
                primary_key = True)
    house_id = Column(Text(length=36), ForeignKey(
                'houses.house_id', ondelete='CASCADE'), 
                primary_key = True)

    price = Column(Numeric(19,2))
    list_date = Column(Date, server_default = func.now())
    status = Column(Text, default = "LISTED")

    def __repr__(self):
        return "Listing(buyer_id={0}, first_name={1}, last_name={2}, email_address={3}, phone_number = {4})".format(self.buyer_id, self.first_name, self.last_name, self.email_address, self.phone_number)

class Sale(Base):  
    __tablename__='sales'  
    sale_id = Column(Text(length=36), primary_key=True)
    listing_id = Column(Text(length=36), ForeignKey(
                'listings.listing_id', ondelete='CASCADE'), 
                primary_key = True)
    buyer_id = Column(Text(length=36), ForeignKey(
                'buyers.buyer_id', ondelete='CASCADE'), 
                primary_key = True)

    price = Column(Numeric(19,2))
    sale_date = Column(Date, server_default = func.now())

    def __repr__(self):
        return "Sale(sale_id={0}, listing_id={1}, buyer_id={2}, price={3}, sale_date = {4})".format(self.sale_id, self.listing_id, self.buyer_id, self.price, self.sale_date)

class Buyer(Base):  
    __tablename__='buyers'  
    buyer_id = Column(Text(length=36), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email_address= Column(String)
    phone_number = Column(String)

    def __repr__(self):
        return "Buyer(buyer_id={0}, first_name={1}, last_name={2}, email_address={3}, phone_number = {4})".format(self.buyer_id, self.first_name, self.last_name, self.email_address, self.phone_number)    

class AgenMonthlyCommission(Base):  
    __tablename__='agentmonthlycommissions'  
    id = Column(Text(length=36), primary_key=True)
    agent_id = Column(Text(length=36), ForeignKey(
                'agents.agent_id', ondelete='CASCADE'), 
                primary_key = True)
    commission_amount = Column(Numeric(19,2))
    start_date = Column(Date, server_default = func.now())
    end_date = Column(Date, server_default = func.now())

    def __repr__(self):
        return "AgentMonthlyCommission(id={0}, agent_id={1}, commission_amount={2}, email_address={3}, phone_number = {4})".format(self.id, self.agent_id, self.commission_amount, self.start_date, self.end_date)

class CommissionRate(Base):  
    __tablename__='commissionrates'  
    id = Column(Text(length=36), primary_key=True)
    price_min = Column(Numeric(19,2), nullable=False)
    price_max = Column(Numeric(19,2), nullable=False)
    rate = Column(Numeric(3,2), nullable=False)

    def __repr__(self):
        return "Buyer(buyer_id={0}, first_name={1}, last_name={2}, email_address={3}, phone_number = {4})".format(self.buyer_id, self.first_name, self.last_name, self.email_address, self.phone_number)    