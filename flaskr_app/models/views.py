from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_login import current_user
from flask import redirect, url_for

# Didn't end up using these because flask agent didn't work for me. Instead I'm doing it manually with HTML.
class AgentView(ModelView):
    column_list = ('agent_id', 'first_name', 'last_name', 'email_address', 'phone_number')
    column_filters = ('agent_id', 'first_name', 'last_name', 'email_address')
    column_labels = {'agent_id':'ID', 'first_name': 'First Name', 'last_name': 'Last Name','sales':'Houses Bought', 'email_address': 'Email', 'phone_number': "Phone number"}
    column_searchable_list = ['first_name', 'last_name', 'email_address']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self):
        return redirect(url_for('login'))

class OfficeView(ModelView):
    column_list = ('office_id', 'name', 'zipcode')
    column_filters = ('office_id', 'name', 'zipcode')
    column_labels = {'office_id':'ID', 'name': 'Office Name', 'zipcode': 'Zipcode'}
    column_searchable_list = ['name', 'zipcode']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self):
        return redirect(url_for('login'))

class HouseView(ModelView):
    column_list = ('house_id', 'bedrooms_num', 'bathrooms_num', 'zipcode')
    column_filters = ('house_id', 'bedrooms_num', 'bathrooms_num')
    column_labels = {'house_id':'ID', 'bedrooms_num': 'Bedrooms', 'bathrooms_num': 'Bathrooms', 'zipcode':'Zipcode'}
    column_searchable_list = ['bedrooms_num', 'bathrooms_num', 'zipcode']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self):
        return redirect(url_for('login'))

class SellerView(ModelView):
    column_list = ('seller_id', 'first_name', 'last_name', 'email_address', 'phone_number', 'listings')
    column_filters = ('seller_id', 'first_name', 'last_name', 'email_address')
    column_labels = {'seller_id':'ID', 'first_name': 'First Name', 'last_name': 'Last Name','listings':'Houses Listings', 'email_address': 'Email', 'phone_number': "Phone number"}
    column_searchable_list = ['first_name', 'last_name', 'email_address']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self):
        return redirect(url_for('login'))

class BuyersView(ModelView):
    column_list = ('buyer_id', 'first_name', 'last_name', 'email_address', 'phone_number', 'sales')
    column_filters = ('buyer_id', 'first_name', 'last_name', 'email_address')
    column_labels = {'buyer_id':'ID', 'first_name': 'First Name', 'last_name': 'Last Name','sales':'Houses Bought', 'email_address': 'Email', 'phone_number': "Phone number"}
    column_searchable_list = ['first_name', 'last_name', 'email_address']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self):
        return redirect(url_for('login'))

class ListingView(ModelView):
    column_list = ('listing_id', 'price', 'list_date', 'status', 'office', 'seller')
    column_filters = ('price', 'list_date', 'status', 'office.name')
    column_labels = {'listing_id':'ID', 'price': 'Price', 'list_date': 'Date listed','status':'Status', 
                'office.name': 'Office name', 'seller.email': "Seller email"}
    column_searchable_list = ['price', 'status']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self):
        return redirect(url_for('login'))

class SaleView(ModelView):
    column_list = ('sale_id', 'listing_id', 'buyer', 'price', 'sale_date')
    column_filters = ('price', 'sale_date')
    column_labels = {'sale_id':"Sale ID", 'listing_id':'Listing ID', 'price': 'Price Sold', 'sale_date': 'Date Sold','buyer.name':'Buyer'}
    column_searchable_list = ['price', 'sale_date']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self):
        return redirect(url_for('login'))

class AgentMonthlyCommissionView(ModelView):
    column_list = ('agent_id', 'agent.first_name', 'commission_amount', 'start_date', 'end_date')
    column_filters = ('agent.first_name', 'start_date', 'end_date')
    column_labels = {'agent_id':"Agent ID", 'agent.first_name':'Agent Name', 'commission_amount': 'Total Commission Amount', 'start_date': 'Period start date','end_date':'Period end date'}
    column_searchable_list = ['start_date', 'end_date']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self):
        return redirect(url_for('login'))