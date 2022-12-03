
from flaskr_app import app, db
from flask import render_template, request, flash, redirect, url_for
from werkzeug.security import check_password_hash
from flaskr_app.models.models import Admin
from flaskr_app.queries import get_top_agents, get_top_offices, get_monthly_sales_average_price, get_market_days, generate_monthly_commissions

@app.route('/')
def index():
    return render_template('index.html')

# Homepage view of the dashboard with stat summaries. 
@app.route('/dashboard', methods=('GET', 'POST'))
def dashboard():
    if request.method == 'POST':
        month = request.form['month']
        year = request.form['year']

        if int(month) <= 12 and int(month) >= 1 and int(year) >= 0:
            average_sale_price = get_monthly_sales_average_price(month=int(month), year=int(year))
            average_market_time = get_market_days(month=int(month), year=int(year))
            return render_template('dashboard.html', month = month, year = year, average_sale_price = average_sale_price, 
                                    average_sale_duration = average_market_time)

    return render_template('dashboard.html', month = 12, year = 2022, average_sale_price = get_monthly_sales_average_price(month = 12, year = 2022),average_sale_duration = get_market_days(month=12, year=12))


# View code for login.
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        if username == "admin" and password == 'IBelieveICanFly':
            return redirect(url_for('dashboard'))

        # GIVES AN ERROR!!!
        # admin = db.query(Admin)

        # if admin is None:
        #     error = 'Incorrect username.'
        # elif not check_password_hash(admin.password, password):
        #     error = 'Incorrect password.'

        # # Redirect to User's board if login is successful.
        # if error is None:
        #     db.session['user_id'] = admin.admin_id

        #     return redirect(url_for('dashboard'))

        # flash(error)

    return render_template('login.html')


# View code for top 5 agents.
@app.route('/top-agents', methods=('GET', 'POST'))
def top_agents():
    if request.method == 'POST':
        month = request.form['month']
        year = request.form['year']

        if int(month) <= 12 and int(month) >= 1 and int(year) >= 0:
            result = get_top_agents(month=int(month), year=int(year))
            return render_template('top_agents.html', month = month, year = year, agents = result)
            
    return render_template('top_agents.html', month = 12, year = 2022, agents = get_top_agents(month=12, year=2022))


# View code for top 5 offices.
@app.route('/top-offices', methods=('GET', 'POST'))
def top_offices():
    if request.method == 'POST':
        month = request.form['month']
        year = request.form['year']

        if int(month) <= 12 and int(month) >= 1 and int(year) >= 0:
            result = get_top_offices(month=int(month), year=int(year))
            return render_template('top_offices.html', month = month, year = year, offices = result)
            
    return render_template('top_offices.html', month = 12, year = 2022, offices = get_top_offices(month=12, year=2022))



# View code for top 5 offices.
@app.route('/agent-commissions', methods=('GET', 'POST'))
def agent_commission():
    if request.method == 'POST':
        month = request.form['month']
        year = request.form['year']

        if int(month) <= 12 and int(month) >= 1 and int(year) >= 0:
            result = generate_monthly_commissions(month=int(month), year=int(year))
            return render_template('agent_commission.html', month = month, year = year, commissions = result)
            
    return render_template('agent_commission.html', month = 12, year = 2022, commissions = generate_monthly_commissions(month=12, year=2022))