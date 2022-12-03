from flaskr_app.models.models import Agent, Buyer, House, Listing, Sale, Office, Admin
import uuid
from flaskr_app import db

from werkzeug.security import generate_password_hash

def add_admin():
    """A function to create the admin"""
    admin = Admin.query.filter_by(username='admin').first()

    if admin is None:
        admin = Admin(admin_id = str(uuid.uuid4()), username='admin', password = generate_password_hash('IBelieveICanFly'))

        try:
            db.session.add(admin)
            db.session.commit()
        except:
            pass 
        finally: 
            print("Login with: \n username: admin \n password: IBelieveICanFly")
