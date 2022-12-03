from flaskr_app import app, db
from db_data.populate_db import add_admin

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        add_admin()

    app.run(debug=True)