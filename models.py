# Import necessary installs and imports.
import sqlalchemy

# Non-abstract classes.
from sqlalchemy import Table, Column, Text, Integer, ForeignKey, DateTime, select, update, Numeric, String

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