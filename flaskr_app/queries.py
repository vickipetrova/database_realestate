
import time
import calendar
import datetime
from flaskr_app.models.models import Agent, Sale, Listing, Office, House, AgentMonthlyCommission
from sqlalchemy import func, Index
import pandas as pd

# Index created according to the rules discussed here https://stackoverflow.com/questions/107132/what-columns-generally-make-good-indexes
# It is based on the columns that are either in WHERE or JOIN clauses (and aren't primary keys).

# Index for all queries. 
Index('idx_sales_date', Sale.sale_date, Sale.price) # Sale.sale_date is often used to filter the date, Sale.listing_id is already a primary key so not included
                                                    # Sale.price is not crucial but it is often used to order by so it will make the query more efficient - https://stackoverflow.com/questions/16792391/do-i-need-to-add-an-index-on-order-by-field#:~:text=Yes%2C%20index%20will%20help%20you,show%20the%20difference%20in%20execution.

def get_top_agents(db, month, year):
    """
    A query to find the top 5 estate agents who have sold the most (biggest revenue) for the month 
    It includes their contact details and their sales details so that it is easy contact them and congratulate them.
    """

    print("🔄 Generating report for the top 5 agents in the month  of {} - {}... 🔄".format(year, month))
    start_time = time.time()
    try:
        # Get start and end dates
        month_range= calendar.monthrange(year, month)
        start_date = datetime.date(year, month, 1)
        end_date = datetime.date(year, month, month_range[1])

        result = db.session.query(
            Agent.first_name.label('First name'), Agent.last_name.label('Last name'), Agent.phone_number.label('Phone'), Agent.email_address.label('Email'), func.sum(Sale.price).label('Total revenue')
        ).filter(Sale.listing_id == Listing.listing_id, Sale.sale_date.between(start_date, end_date)
        ).filter(Agent.agent_id == Listing.agent_id
        ).group_by(Agent.agent_id).order_by(func.sum(Sale.price).desc()).limit(5).all()
        
        print("🔝🧍 Top 5 agents of the month {} - {} 🧍🔝".format(year, month))
        df = pd.DataFrame(result)
        print(df)

        return result

    except:
        db.session.rollback()
        raise
    finally:
        print("✅ Finished generating report in {} seconds ✅".format(round(time.time() - start_time, 3)))


def get_top_offices(db, month, year):
    """
    A query to find the top 5 officces that sold the most (biggest total revenue) for the month 
    """
    print("🔄 Generating report for the top 5 offices in the month  of {} - {}... 🔄".format(year, month))
    start_time = time.time()
    try:
        # Get start and end dates
        month_range= calendar.monthrange(year, month)
        start_date = datetime.date(year, month, 1)
        end_date = datetime.date(year, month, month_range[1])

        result = db.session.query(
            Office.office_id.label('Office ID'), Office.name.label('Office Name'), Office.zipcode.label('Zipcode'), func.sum(Sale.price).label('Total revenue')
        ).filter(Sale.listing_id == Listing.listing_id, Sale.sale_date.between(start_date, end_date)
        ).filter(Office.office_id == Listing.office_id
        ).group_by(Office.office_id).order_by(func.sum(Sale.price).desc()).limit(5).all()
        
        print("🔝🏢 Top 5 offices of the month {} - {} 🏢🔝".format(year, month))
        df = pd.DataFrame(result)
        print(df)
        return result

    except:
        db.session.rollback()
        raise
    finally:
        print("✅ Finished generating report in {} seconds ✅".format(round(time.time() - start_time, 3)))


def get_monthly_sales_average_price(db, month, year):
    """
    A query that calculates the average selling price for all houses that were sold that month.
    """

    print("🔄 Calculating the avergae price of the houses sold in the month  of {} - {}... 🔄".format(year, month))
    start_time = time.time()

    try:
        # Get start and end dates
        month_range= calendar.monthrange(year, month)
        start_date = datetime.date(year, month, 1)
        end_date = datetime.date(year, month, month_range[1])

        result = db.session.query(
            func.avg(Sale.price)
        ).filter(Sale.sale_date.between(start_date, end_date)).all()

        if result[0][0] is None:
            print("No houses were sold this month.")
            print("💰The average selling price for all houses that were sold in the month {} - {} was 0 dollars 💰".format(year, month))
            return 0
        else:
            print("💰The average selling price for all houses that were sold in the month {} - {} was {} dollars 💰".format(year, month, result[0]))
            return round(result[0][0],2)
    except:
        db.session.rollback()
        raise
    finally:
        print("✅ Finished query in {} seconds ✅".format(round(time.time() - start_time, 3)))


def get_market_days(db, month, year):

    print("🔄 Calculating average time spent on the market for the sales in the month  of {} - {}... 🔄".format(year, month))
    start_time = time.time()
    try:
        # Get start and end dates
        month_range= calendar.monthrange(year, month)
        start_date = datetime.date(year, month, 1)
        end_date = datetime.date(year, month, month_range[1])

        result = db.session.query(
            Listing.list_date, Sale.sale_date, House.house_id, House.zipcode
        ).filter(Sale.listing_id == Listing.listing_id, Sale.sale_date.between(start_date, end_date)
        ).filter(Listing.house_id == House.house_id).all()

        if len(result) == 0:
            print(" No houses sold in the month {} - {} 📆".format(year, month))
            return 0
        
        days_on_market = [(listing[1]-listing[0]).days for listing in result]
        average_days_on_market = sum(days_on_market)/len(result)
        print(" The average days on the market for houses in the month {} - {} was {} days📆".format(year, month, average_days_on_market))

        return round(average_days_on_market,2)
    except:
        db.session.rollback()
        raise
    finally:
        print("✅ Finished query in {} seconds ✅".format(round(time.time() - start_time, 3)))


def generate_monthly_commissions(db, month, year):
    """
    A query to calculate the commission that each estate agent must receive and store the results in a separate table called AgentMonthlyCommission.

    I think there might by an error in this query but I haven't been able to catch it. It was working at first but then I made the app more complex.
    I think it might have something to do with the if statements. It always loads the same commissions reagrdless of the month. 
    """

    print("🔄 Generating report for the agent commissions in the month  of {} - {}... 🔄".format(year, month))
    start_time = time.time()
    try:
        
        # Get start and end dates
        month_range= calendar.monthrange(year, month)
        start_date = datetime.date(year, month, 1)
        end_date = datetime.date(year, month, month_range[1])

        
        # I assume that all data points were recorded before this query was ran since I insert the random data once in the beginning. 
        # If previously was ran a report for 2022/12, and then a new sale is added in 2022/12, the report will not update.  
        # This can be improved since for a real database app the admin will want to record new sales but for the purposes of this assignment I've left it like this. 
        # Another option is to delete the table entries and then generate a new report every time the function is called. 

        # Check if report is already generated (meaning there are agent commission entries for that period).
        agent_commissions = db.session.query(
            AgentMonthlyCommission.agent_id
            ).filter(AgentMonthlyCommission.start_date == start_date, AgentMonthlyCommission.end_date == end_date).all()
        
        # If table entries not created before, create them. 
        if not agent_commissions:

            # Get all agents.
            agents = db.session.query(Agent).all()

            # Initialize all agent monthly comissions to 0.
            agent_monthly_commissions = []
            for agent in agents:
                agent_monthly_commission = AgentMonthlyCommission(agent_id = agent.agent_id, commission_amount = 0, start_date = start_date, end_date = end_date)
                agent_monthly_commissions.append(agent_monthly_commission)

            db.session.add_all(agent_monthly_commissions)

            # Get all agent sales (agent id and sale price) for the given period.
            agent_sales = db.session.query(
                Listing.agent_id, Sale.price
                ).filter(Listing.listing_id == Sale.listing_id, Sale.sale_date.between(start_date, end_date)).all()

            # If any sales occured that month, update the relevant agent commission.
            if agent_sales is not None:                
                # Go over the sales and update the agent commission value accordingly.
                for sale in agent_sales:
                    # Get commission amount for the sale.
                    commission_amount = calculate_agent_commission(float(sale[1]))
                    # Get row of agent commission table and update its value.
                    agent_commission_entry = db.session.query(AgentMonthlyCommission).filter(AgentMonthlyCommission.agent_id == sale[0], 
                                                AgentMonthlyCommission.start_date == start_date, AgentMonthlyCommission.end_date == end_date).one()
                    agent_commission_entry.commission_amount += commission_amount

                    db.session.add(agent_commission_entry)

                db.session.commit()

        print("🧾 Agent monthly commissions for {} - {} 🧾".format(year, month))
        result = db.session.query (
            Agent.agent_id, Agent.first_name, Agent.last_name, AgentMonthlyCommission.commission_amount
        ).filter(Agent.agent_id == AgentMonthlyCommission.agent_id, AgentMonthlyCommission.start_date == start_date,AgentMonthlyCommission.end_date == end_date).all()
        
        # Format output nicely.
        df = pd.DataFrame(result)
        print(df)
        return result

    except:
        db.session.rollback()
        raise
    finally:
        print("✅ Finished generating report in {} seconds ✅".format(round(time.time() - start_time, 3)))


def calculate_agent_commission(sale_price):
    """
    A function to calculate the agent commission based on the price of the sale.
    
    Possible improvement: right now I convert the the sale price to float before passing it because otherwise I get a warning. 
    This is because SQLAclhemy/SQLite doesn't support Decimal data types which can lead to rounding errors. A solution online was to store
    price (money) as integers or better as strings. 
    I found out about this too late and I remember in class we discussed that we can also use Numeric type and be careful about rounding and digits.
    """
    if sale_price < 100_000:
        return sale_price*0.1
    elif sale_price < 200_000:
        return sale_price*0.075
    elif sale_price < 500_000:
        return sale_price*0.06
    elif sale_price < 1_000_000:
        return sale_price*0.05
    else:
        return sale_price*0.04
