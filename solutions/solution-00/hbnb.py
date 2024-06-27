""" Another way to run the app"""

from src import create_app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        from .src.db import db

        print("Creating database tables...")
        db.create_all()
        print("Tables created.")

    app.run()
