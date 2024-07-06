""" Populate the database with some data at the start of the application"""
from src.persistence.repository import Repository


def populate_memory(repo: Repository) -> None:
    """Populates the db with a dummy country"""
    from src.models.country import Country

    countries = [
        Country(name="Uruguay", code="UY"),
    ]

    for country in countries:
        repo.save(country)

    print("Memory DB populated")


def populate_db(repo: Repository) -> None:
    """Populates the db with a dummy country"""
    from src.models.db.country import Country

    countries = [
        Country(name="Uruguay", country_code="UY"),
        Country(name="United-State", country_code="US")
    ]
    countries_all = repo.db.session.query(Country).all()
    countries_codes = [country.country_code for country in countries_all]

    for country in countries:
        if country.country_code not in countries_codes:
            try:
                repo.save(country)
            except Exception:
                pass
    print("DB populated")
