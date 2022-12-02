import calendar
import datetime
import time
import sqlalchemy
import pandas as pd
from db.models import AgentMonthlyCommission, Agent, agent_to_office, Buyer, CommissionRate, House, Seller, Listing, Sale, Office
from sqlalchemy import func

def get_top_offices(session, month, year):
    """
    A query to find the top 5 officces that sold the most (biggest total revenue) for the month 
    """
    print("🔄 Generating report for the top 5 offices in the month  of {} - {}... 🔄".format(year, month))
    start_time = time.time()
    try:
        # Get start and end dates
        month_range= calendar.monthrange(year, month)
        start_date = datetime.date(year, month, month_range[0])
        end_date = datetime.date(year, month, month_range[1])

        result = session.query(
            Office.office_id.label('Office ID'), Office.name.label('Office Name'), Office.zipcode.label('Zipcode'), func.sum(Sale.price).label('Total revenue')
        ).filter(Sale.listing_id == Listing.listing_id, Sale.sale_date.between(start_date, end_date)
        ).filter(Office.office_id == Listing.office_id
        ).group_by(Office.office_id).order_by(func.sum(Sale.price).desc()).limit(5).all()
        
        print("🔝🏢 Top 5 offices of the month {} - {} 🏢🔝".format(year, month))
        df = pd.DataFrame(result)
        print(df)

    except:
        session.rollback()
        raise
    finally:
        print("✅ Finished generating report in {} seconds ✅".format(round(time.time() - start_time, 3)))
        
def get_top_agents(session, month, year):
    """
    A query to find the top 5 estate agents who have sold the most (biggest revenue) for the month 
    It includes their contact details and their sales details so that it is easy contact them and congratulate them.
    """
    print("🔄 Generating report for the top 5 agents in the month  of {} - {}... 🔄".format(year, month))
    start_time = time.time()
    try:
        # Get start and end dates
        month_range= calendar.monthrange(year, month)
        start_date = datetime.date(year, month, month_range[0])
        end_date = datetime.date(year, month, month_range[1])

        result = session.query(
            Agent.first_name.label('First name'), Agent.last_name.label('Last name'), Agent.phone_number.label('Phone'), Agent.email_address.label('Email'), func.sum(Sale.price).label('Total revenue')
        ).filter(Sale.listing_id == Listing.listing_id, Sale.sale_date.between(start_date, end_date)
        ).filter(Agent.agent_id == Listing.agent_id
        ).group_by(Agent.agent_id).order_by(func.sum(Sale.price).desc()).limit(5).all()
        
        print("🔝🧍 Top 5 agents of the month {} - {} 🧍🔝".format(year, month))
        df = pd.DataFrame(result)
        print(df)

    except:
        session.rollback()
        raise
    finally:
        print("✅ Finished generating report in {} seconds ✅".format(round(time.time() - start_time, 3)))


def generate_monthly_commissions(session, month, year):
    """
    A query to calculate the commission that each estate agent must receive and store the results in a separate table called AgentMonthlyCommission.
    """

    print("🔄 Generating report for the agent commissions in the month  of {} - {}... 🔄".format(year, month))
    start_time = time.time()
    try:
        
        # Get start and end dates
        month_range= calendar.monthrange(year, month)
        start_date = datetime.date(year, month, month_range[0])
        end_date = datetime.date(year, month, month_range[1])

        # Check if report is already generated. 
        agent_sales = session.query(
            AgentMonthlyCommission.agent_id
            ).filter(AgentMonthlyCommission.start_date == start_date, AgentMonthlyCommission.end_date == end_date).all()
        
        if not agent_sales:
            agents = session.query(Agent).all()

            # Initialize all agent monthly comissions to 0.
            agent_monthly_commissions = []
            for agent in agents:
                agent_monthly_commission = AgentMonthlyCommission(agent_id = agent.agent_id, commission_amount = 0, start_date = start_date, end_date = end_date)
                agent_monthly_commissions.append(agent_monthly_commission)

            session.add_all(agent_monthly_commissions)

            # Get all agent sales by id and sale price.
            agent_sales = session.query(
                Listing.agent_id, sqlalchemy.func.sum(Sale.price)
                ).filter(Listing.listing_id == Sale.listing_id, Sale.sale_date.between(start_date, end_date)).all()

            # Go over the sales and update the agent commission value accordinlgy.
            for sale in agent_sales:
                commission_amount = calculate_agent_commission(sale[1])
                agent_commission_entry = session.query(AgentMonthlyCommission).filter(AgentMonthlyCommission.agent_id == sale[0], 
                                            AgentMonthlyCommission.start_date == start_date, AgentMonthlyCommission.end_date == end_date).one()
                agent_commission_entry.commission_amount += commission_amount

            session.add_all(agent_monthly_commissions)

            session.commit()

        print("🧾 Agent monthly commissions for {} - {} 🧾".format(year, month))
        result = session.query (
            Agent.agent_id, Agent.first_name, Agent.last_name, AgentMonthlyCommission.commission_amount
        ).filter(Agent.agent_id == AgentMonthlyCommission.agent_id)
        
        df = pd.DataFrame(result)
        print(df)

    except:
        session.rollback()
        raise
    finally:
        print("✅ Finished generating report in {} seconds ✅".format(round(time.time() - start_time, 3)))

def calculate_agent_commission(sale_price):
    if sale_price < 100_000:
        return float(sale_price)*0.1
    elif sale_price < 200_000:
        return sale_price*0.075
    elif sale_price < 500_000:
        return sale_price*0.06
    elif sale_price < 1_000_000:
        return sale_price*0.05
    else:
        return sale_price*0.04


def get_market_days(session, month, year):

    print("🔄 Calculating average time spent on the market for the sales in the month  of {} - {}... 🔄".format(year, month))
    start_time = time.time()
    try:
        # Get start and end dates
        month_range= calendar.monthrange(year, month)
        start_date = datetime.date(year, month, month_range[0])
        end_date = datetime.date(year, month, month_range[1])

        result = session.query(
            Listing.list_date, Sale.sale_date, House.house_id, House.zipcode
        ).filter(Sale.listing_id == Listing.listing_id, Sale.sale_date.between(start_date, end_date)
        ).filter(Listing.house_id == House.house_id).all()
        
        days_on_market = [(listing[1]-listing[0]).days for listing in result]
        average_days_on_market = sum(days_on_market)/len(result)
        print(" The average days on the market for houses in the month {} - {} was {} days📆".format(year, month, average_days_on_market))
    except:
        session.rollback()
        raise
    finally:
        print("✅ Finished query in {} seconds ✅".format(round(time.time() - start_time, 3)))
    
def get_monthly_sales_average_price(session, month, year):
    """
    A query that calculates the average selling price for all houses that were sold that month.
    """

    print("🔄 Calculating the avergae price of the houses sold in the month  of {} - {}... 🔄".format(year, month))
    start_time = time.time()

    try:
        # Get start and end dates
        month_range= calendar.monthrange(year, month)
        start_date = datetime.date(year, month, month_range[0])
        end_date = datetime.date(year, month, month_range[1])

        result = session.query(
            func.avg(Sale.price)
        ).filter(Sale.sale_date.between(start_date, end_date)).one()

        if result[0] is None:
            print("No houses were sold this month.")
            print("💰The average selling price for all houses that were sold in the month {} - {} was 0 dollars 💰".format(year, month))
        else:
            print("💰The average selling price for all houses that were sold in the month {} - {} was {} dollars 💰".format(year, month, result[0]))
    except:
        session.rollback()
        raise
    finally:
        print("✅ Finished query in {} seconds ✅".format(round(time.time() - start_time, 3)))