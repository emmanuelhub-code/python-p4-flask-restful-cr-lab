import pytest
import json
from app import app, db, Plant  # import your app, db, and model

# -------------------------------
# Test Client Fixture
# -------------------------------
@pytest.fixture
def client():
    # Use an in-memory database for testing
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()  # Create tables
        yield app.test_client()  # Provide test client
        db.drop_all()  # Clean up after tests

# -------------------------------
# Test Plant Model
# -------------------------------
def test_plants_get_route_returns_list_of_plant_objects(client):
    # Create a plant
    with app.app_context():
        p = Plant(
            name="Douglas Fir",
            image="https://example.com/douglas-fir.png",
            price=10.0
        )
        db.session.add(p)
        db.session.commit()

    # Make GET request
    response = client.get("/plants")
    data = json.loads(response.data.decode())

    assert response.status_code == 200
    assert isinstance(data, list)
    assert data[0]["name"] == "Douglas Fir"

def test_plants_post_route_creates_plant_record_in_db(client):
    # POST a new plant
    response = client.post(
        "/plants",
        json={
            "name": "Live Oak",
            "image": "https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx",
            "price": 250.00,
        }
    )

    assert response.status_code == 201  # make sure your route returns 201 on success

    # Verify in DB
    with app.app_context():
        lo = Plant.query.filter_by(name="Live Oak").first()
        assert lo is not None
        assert lo.price == 250.00

def test_plant_by_id_get_route(client):
    # Insert a plant
    with app.app_context():
        p = Plant(
            name="Maple",
            image="https://example.com/maple.png",
            price=15.0
        )
        db.session.add(p)
        db.session.commit()
        plant_id = p.id

    # GET by ID
    response = client.get(f"/plants/{plant_id}")
    assert response.status_code == 200

def test_plant_by_id_get_route_returns_one_plant(client):
    # Insert a plant
    with app.app_context():
        p = Plant(
            name="Oak",
            image="https://example.com/oak.png",
            price=20.0
        )
        db.session.add(p)
        db.session.commit()
        plant_id = p.id

    # GET by ID
    response = client.get(f"/plants/{plant_id}")
    data = json.loads(response.data.decode())

    assert data["name"] == "Oak"
    assert data["price"] == 20.0
