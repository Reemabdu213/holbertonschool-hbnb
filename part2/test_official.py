#!/usr/bin/env python3
"""Test according to official instructions"""

print("Testing according to official instructions\n")
print("="*60)

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

print("\n1. Testing User Creation...")

def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False
    print("User creation test passed!")

test_user_creation()

print("\n2. Testing Place Creation with Relationships...")

def test_place_creation():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    
    review = Review(
        text="Great stay!",
        rating=5,
        place=place,
        user=owner
    )
    place.add_review(review)
    
    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    print("Place creation and relationship test passed!")

test_place_creation()

print("\n3. Testing Amenity Creation...")

def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    print("Amenity creation test passed!")

test_amenity_creation()

print("\n" + "="*60)
print("All tests passed!\n")
