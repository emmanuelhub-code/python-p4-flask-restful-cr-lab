from app import db, Plant

# Create tables if they don't exist
db.create_all()

# Seed data
plants = [
    Plant(name="Aloe", image="https://via.placeholder.com/150?text=Aloe", price=11.50),
    Plant(name="ZZ Plant", image="https://via.placeholder.com/150?text=ZZ+Plant", price=25.98)
]

db.session.add_all(plants)
db.session.commit()

print("Database seeded!")
