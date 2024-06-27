from sqlalchemy import inspect
from src.db import db
from src import create_app
from src.models.db.amenity import Amenity
from src.controllers.amenities import get_amenities

def run_tests():
    app = create_app()
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Tables created.")

        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Tables in the database: {tables}")

        Amenity.create({
            "name": "WiFi"
        })
        print("Added new amenity.")

        amenities: list[Amenity] = Amenity.get_all()
        print(amenities)
        for amenity in amenities:
            print(f"Amenity: {amenity.name}")
        amenities = get_amenities()
        print(amenities)

if __name__ == "__main__":
    run_tests()