# About this repo: Real Estate Head Office Database

This is a database for a hypothetical Real Estate Head Office. It was created for an assignments for my CS162: SOftware engineering course. The original assignment description can be found here: https://github.com/minerva-university/cs162/blob/main/assignments/4_database.md

## Description

You have been tasked with building a database system for a large franchised real
estate company. This means that the company has many offices located all over
the country. Each office is responsible for selling houses in a particular area.
However an estate agent can be associated with one or more offices.

### Inserting data
1. Whenever a house is listed then the following things need to happen:
 -  All the relevant details of that house need to be captured, ie. at least: seller details, # of bedrooms, # of bathrooms, listing price, zip code, date of listing, the listing estate agent, and the appropriate office.
2. Whenever a house is sold then the following things need to happen:
 - The estate agent commission needs to be calculated. This happens on a sliding scale:
   - For houses sold below $100,000 the commission is 10%
   - For houses between $100,000 and $200,000 the commission is 7.5%
   - For houses between $200,000 and $500,000 the commission is 6%
   - For houses between $500,000 and $1,000,000 the commission is 5%
   - For houses above $1,000,000 the commission is 4%
 - All appropriate details related to the sale must be captured, ie. at least: buyer details, sale price, date of sale, the selling estate agent.
 - The original listing must be marked as sold.

### Querying data
Every month the following reports need to be run:
 - Find the top 5 offices with the most sales for that month.
 - Find the top 5 estate agents who have sold the most for the month (include their contact details and their sales details so that it is easy contact them and congratulate them).
 - Calculate the commission that each estate agent must receive and store the results in a separate table. 
 - For all houses that were sold that month, calculate the average number of days on the market.
 - For all houses that were sold that month, calculate the average selling price

### Testing:
To test your solution you will need to create fictitious data and ensure that the correct results are calculated from your SQL code.


# Running the app

## MacOS

Use the following commands to initialize the databse and run the app. You can copy-paste all commands at once in the terminal:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py
```
Then open another terminal to load the randomly generated data.
```bash
python3 insert_data.py
```

Reload the app in the browser to load the data. 

# Running the tests

## MacOS

Use the following commands to initialize the databse and run the app. You can copy-paste all commands at once in the terminal:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 test.py
```

# UML Diagram of the Database Schema
![UML](uml.png "UML Diagram")