import pytest
from server import app
from unittest.mock import patch


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_clubs():
    return [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"}
    ]


@pytest.fixture
def test_competitions():
    return [
        {
            "name": "Spring Festival",
            "date": "2026-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2023-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]


@pytest.fixture(autouse=True)
def _mock_data(test_clubs, test_competitions):
    """Automatically patch clubs and competitions in all tests"""
    with patch('server.clubs', [club.copy() for club in test_clubs]), \
         patch('server.competitions', [comp.copy() for comp in test_competitions]):
        yield
