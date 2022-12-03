from flaskr_app import db

# Import necessary installs and imports.
from sqlalchemy.sql import func

# Assossiaction table between Agent and Office class for many-to-many relationship.
# Documentation: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
agent_to_office = db.Table('agent_to_office',
    db.Column('agent_id', db.Text(length=36), db.ForeignKey(
                'agents.agent_id', ondelete='CASCADE')),
    db.Column('office_id', db.Text(length=36), db.ForeignKey(
                'offices.office_id', ondelete='CASCADE'))
)

class Agent(db.Model):  # Python class name
    __tablename__='agents'  # SQL table name
    agent_id = db.Column(db.Text(length=36), primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone_number = db.Column(db.String)
    email_address = db.Column(db.String)

    offices = db.relationship("Office", secondary=agent_to_office, back_populates = 'agents') #many to many - an agent can work for many offices and an office can have many agents working for it
    listings = db.relationship("Listing") #one to many - a listing can have one agent linked to it but an agent can have multiple listings
    commissions = db.relationship("AgentMonthlyCommission", back_populates = "agent") #one to many - an agent can have multiple commissions - one for each month of the year, a commission is linked to a single agent

    def __repr__(self):
        return "Agent(agent_id={0}, first_name={1}, last_name={2}, phone_number={3}, email_address={4})".format(self.agent_id, self.first_name, self.last_name, self.phone_number, self.email_address)

    __table_args__ = {'extend_existing': True}


class Office(db.Model):
    __tablename__ = 'offices'
    office_id = db.Column(db.Text(length=36), primary_key=True)
    name = db.Column(db.String)
    zipcode = db.Column(db.Integer)

    agents = db.relationship("Agent", secondary=agent_to_office, back_populates = 'offices') #many to many - an agent can work for many offices and an office can have many agents working for it
    listings = db.relationship("Listing", back_populates = "office") #one to many - one office can have many listings, but a listing can be only from a single office

    def __repr__(self):
        return "Office(office_id={0}, name = {1}, zipcode={2})".format(self.office_id, self.name, self.zipcode)

    __table_args__ = {'extend_existing': True}

class House(db.Model):  
    __tablename__='houses'  
    house_id = db.Column(db.Text(length=36), primary_key=True)
    bedrooms_num = db.Column(db.Integer)
    bathrooms_num = db.Column(db.Integer)
    zipcode = db.Column(db.Integer)

    listings = db.relationship("Listing") #one to many - a listing is linked to a single house, but a house can be linked to multiple listings - 
                                    #e.g. selling it for different prices at two different offices or by two different agents (an office in LA might sell it for more money than an office in a small town) 

    def __repr__(self):
        return "House(house_id={0}, bedrooms_num={1}, bathrooms_num={2}, zipcode={3})".format(self.house_id, self.bedrooms_num, self.bathrooms_num, self.zipcode)

class Seller(db.Model):  
    __tablename__='sellers'  
    seller_id = db.Column(db.Text(length=36), primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email_address= db.Column(db.String)
    phone_number = db.Column(db.String)

    listings = db.relationship("Listing", back_populates = 'seller') #one to many - one seller can sell multiple listings, but a listing can be sold by a single seller 
                                #possible point for improvement e.g. what if it's a married couple selling a property, not sure how it works legally - I assume there is a single seller

    def __repr__(self):
        return "Seller(seller_id={0}, first_name={1}, last_name={2}, email_address={3}, phone_number = {4})".format(self.seller_id, self.first_name, self.last_name, self.email_address, self.phone_number)

    __table_args__ = {'extend_existing': True}

class Buyer(db.Model):  
    __tablename__='buyers'  
    buyer_id = db.Column(db.Text(length=36), primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email_address= db.Column(db.String)
    phone_number = db.Column(db.String)

    sales = db.relationship("Sale", back_populates = "buyer")#one to many - a buyer can buy many different listings (linked to multiple sales) but a sale can only be linked to a single buyer 
                    #(I assume this to be the case, not sure how it works leaglly with married couples for example)

    def __repr__(self):
        return "Buyer(buyer_id={0}, first_name={1}, last_name={2}, email_address={3}, phone_number = {4})".format(self.buyer_id, self.first_name, self.last_name, self.email_address, self.phone_number)


class Listing(db.Model):  
    __tablename__='listings'  
    listing_id = db.Column(db.Text(length=36), primary_key=True)
    agent_id = db.Column(db.Text(length=36), db.ForeignKey(
                'agents.agent_id', ondelete='CASCADE')) #one to many - a listing can have one agent linked to it but an agent can have multiple listings
    office_id = db.Column(db.Text(length=36), db.ForeignKey(
                'offices.office_id', ondelete='CASCADE')) #one to many - one office can have many listings, but a listing can be only from a single office
    seller_id = db.Column(db.Text(length=36), db.ForeignKey(
                'sellers.seller_id', ondelete='CASCADE')) #one to many - one seller can sell multiple listings, but a listing can be sold by a single seller 
                                    #possible point for improvement e.g. what if it's a married couple selling a property - I assume there is a single seller
    house_id = db.Column(db.Text(length=36), db.ForeignKey(
                'houses.house_id', ondelete='CASCADE')) #one to many - a listing is linked to a single house, but a house can be linked to multiple listings - 
                                    #e.g. selling it for different prices at two different offices or by two different agents (an office in LA might sell it for more money than an office in a small town)
    
    price = db.Column(db.Numeric(19,2))
    list_date = db.Column(db.Date, server_default = func.now())
    status = db.Column(db.Text, default = "LISTED")

    office = db.relationship("Office", back_populates = "listings")
    seller = db.relationship("Seller", back_populates = "listings")

    def __repr__(self):
        return "Listing(listing_id={0}, agent_id={1}, office_id={2}, seller_id={3}, house_id = {4}, price = {5}, list_date = {6}, status = {7})".format(self.listing_id, self.agent_id, self.office_id, self.seller_id, self.house_id, self.price, self.list_date, self.status)

class Sale(db.Model):  
    __tablename__='sales'  
    sale_id = db.Column(db.Text(length=36), primary_key=True)
    listing_id = db.Column(db.Text(length=36), db.ForeignKey(
                'listings.listing_id', ondelete='CASCADE'), 
                primary_key = True) #
    buyer_id = db.Column(db.Text(length=36), db.ForeignKey(
                'buyers.buyer_id', ondelete='CASCADE'))

    buyer = db.relationship("Buyer", back_populates="sales")

    price = db.Column(db.Numeric(19,2))
    sale_date = db.Column(db.Date, server_default = func.now())

    def __repr__(self):
        return "Sale(sale_id={0}, listing_id={1}, buyer_id={2}, price={3}, sale_date = {4})".format(self.sale_id, self.listing_id, self.buyer_id, self.price, self.sale_date)


class AgentMonthlyCommission(db.Model):  
    __tablename__='agentmonthlycommissions'  
    agent_id = db.Column(db.Text(length=36), db.ForeignKey(
                'agents.agent_id', ondelete='CASCADE'), 
                primary_key = True)
    agent = db.relationship("Agent", back_populates = 'commissions')
    commission_amount = db.Column(db.Numeric(19,2))
    start_date = db.Column(db.Date, server_default = func.now(), primary_key = True)
    end_date = db.Column(db.Date, server_default = func.now(), primary_key = True)

    def __repr__(self):
        return "AgentMonthlyCommission(agent_id={0}, commission_amount={1}, start_date={2}, end_date = {3})".format(self.agent_id, self.commission_amount, self.start_date, self.end_date)

# Admin table 
class Admin(db.Model):  
    __tablename__='admins'  
    admin_id = db.Column(db.Text(length=36), primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    __table_args__ = {'extend_existing': True}