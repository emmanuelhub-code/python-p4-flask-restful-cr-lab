import pytest
from app import app, db
from models import Plant

@pytest.fixture(scope="module")
def test_client():
    # Use in-memory SQLite DB
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

class TestPlant:

    def test_can_be_created(self, test_client):
        with app.app_context():
            p = Plant(
                name="Douglas Fir",
                image="https://example.com/douglas-fir.png",
                price=10.0
            )
            db.session.add(p)
            db.session.commit()

            assert p.id is not None

    def test_can_be_retrieved(self, test_client):
        with app.app_context():
            p = Plant.query.filter_by(name="Douglas Fir").first()
            assert p is not None
            assert p.image == "https://example.com/douglas-fir.png"
