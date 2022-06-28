from flask_migrate import Migrate
from api import create_app
from api.models import db

# sets up the app
app = create_app()

migrate = Migrate(app, db)


def runserver():
    app.run(debug=True, host="0.0.0.0", port=5000)


def runworker():
    app.run(debug=False)


def recreate_db():
    """
    Recreates a database. This should only be used once
    when there's a new database instance. This shouldn't be
    used when you migrate your database.
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()


def get_app_map():
    print(app.url_map)


if __name__ == "__main__":
    # recreate_db()
    runserver()
