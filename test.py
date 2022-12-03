import unittest
from flask_testing import TestCase
from flask import Flask
from flaskr_app import db, queries
from test_data import test_data


class AppTest(TestCase):

    def create_app(self):
        """
        Initialize flask app for testing.
        """
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['TESTING'] = True

        return self.app

    def setUp(self):
        """
        Create test data to run the tests on. 
        """
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            # Generate the test data.
            test_data(db) 


    def test_monthly_sales_average_price1(self):
        """Tests the get_monthly_sales_average_price query function when there are sales in the month."""

        result = queries.get_monthly_sales_average_price(db = db, month = 12, year = 2022)

        self.assertEqual(10000, result)

    def test_monthly_sales_average_price2(self):
        """Tests the get_monthly_sales_average_price query function when there are NO sales in the month."""

        result = queries.get_monthly_sales_average_price(db = db, month = 11, year = 2022)

        self.assertEqual(0, result)

    def test_sale_duration1(self):
        """Tests the get_market_days query function when there are sales in the month."""

        result = queries.get_market_days(db = db, month = 12, year = 2022)

        # all listings were created on 2022/12/1  and all were sold on 2022/12/3 which is 2 days
        self.assertEqual(2, result)

    def test_sale_duration2(self):
        """Tests the get_market_days query function when there are NO sales in the month."""

        result = queries.get_market_days(db = db, month = 11, year = 2022)

        self.assertEqual(0, result)

    def test_top_agents1(self):
        """Tests the get_top_agents query function when there are NO sales in the month."""

        #fetch sql query result
        result = queries.get_top_agents(db = db, month = 11, year = 2022)
        
        # No sales that month so 0 top agents. 
        self.assertEqual(0, len(result))

    def test_top_agent2(self):
        """Tests the get_top_agents query function when there are sales in the month."""

        #fetch sql query result
        result = queries.get_top_agents(db = db, month = 12, year = 2022)
        
        # Only 1 agent with sales that month.
        self.assertEqual(1, len(result))
        # Check he has the correct total commission - 3 sales with sale price of 10000 each.
        self.assertEqual(10000*3, float(result[0][4]))

    def test_top_offices(self):
        """Tests the get_top_offices query function """
        #fetch sql query result
        result = queries.get_top_offices(db = db, month = 12, year = 2022)

        # 3 sales with 3 different offices that month so it should be 3 offices in top 5
        self.assertEqual(3, len(result))
        # Check that offices have correct revenue.
        self.assertEqual(10000, float(result[0][3]))
        self.assertEqual(10000, float(result[1][3]))
        self.assertEqual(10000, float(result[2][3]))

    def test_agent_commission1(self):
        """Tests the agent commission table and query function """
        result = queries.generate_monthly_commissions(db = db, month = 12, year = 2022)
        # Check that commissions loaded for all 5 agents
        self.assertEqual(5, len(result))
        # First agent sold 3 sales of 10_0000 each - check correct commission.
        self.assertEqual(10000*0.1*3, float(result[0][3]))
        # The second row should have 0 commission (no sales)
        self.assertEqual(0, result[1][3])

    def test_agent_commission2(self):
        """Tests the agent commission table and query function """
        result = queries.generate_monthly_commissions(db = db, month = 11, year = 2022)
        # Check that commissions loaded for all 5 agents
        self.assertEqual(5, len(result))
        # No agent sold anything
        self.assertEqual(0, float(result[0][3]))
        self.assertEqual(0, float(result[1][3]))
        self.assertEqual(0, float(result[2][3]))
        self.assertEqual(0, result[1][3])
        self.assertEqual(0, float(result[4][3]))

if __name__ == '__main__':
    unittest.main()