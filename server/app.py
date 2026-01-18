from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Plant

app = Flask(__name__)

# DATABASE: change path if needed
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ===== Routes =====

# GET all plants
@app.route("/plants", methods=["GET"])
def get_plants():
    plants = Plant.query.all()
    return jsonify([p.to_dict() for p in plants]), 200

# GET one plant by id
@app.route("/plants/<int:plant_id>", methods=["GET"])
def get_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    return jsonify(plant.to_dict()), 200

# POST create new plant
@app.route("/plants", methods=["POST"])
def create_plant():
    data = request.get_json()
    new_plant = Plant(
        name=data["name"],
        image=data["image"],
        price=data["price"]
    )
    db.session.add(new_plant)
    db.session.commit()
    return jsonify(new_plant.to_dict()), 201

# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
