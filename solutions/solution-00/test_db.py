from sqlalchemy import inspect
from src.db import db
from src import create_app
from src.models.db.amenity import Amenity

def run_tests():
    app = create_app()
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Tables created.")

        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Tables in the database: {tables}")

        new_amenity = Amenity(name='WiFi')
        new_amenity.save()
        print("Added new amenity.")

        amenities = db.session.query(Amenity).all()
        for amenity in amenities:
            print(f"Amenity: {amenity.name}")

if __name__ == "__main__":
    run_tests()