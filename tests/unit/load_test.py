from unittest.mock import mock_open, patch
import server


def test_load_clubs():
    """Test that load_clubs loads the club data correctly from JSON file"""
    mock_json_content = """{
        "clubs": [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
            {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"}
        ]
    }"""

    with patch("builtins.open", mock_open(read_data=mock_json_content)):
        clubs = server.load_clubs()

        assert isinstance(clubs, list)
        assert len(clubs) == 2
        assert clubs[0] == {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}
        assert clubs[0]["name"] == "Simply Lift"
        assert clubs[1]["email"] == "admin@irontemple.com"


def test_load_competitions():
    """Test that load_competitions loads competition data correctly from JSON file"""
    mock_json_content = """{
        "competitions": [
            {"name": "Spring Festival", "date": "2026-03-27 10:00:00", "numberOfPlaces": "25"},
            {"name": "Fall Classic", "date": "2023-10-22 13:30:00", "numberOfPlaces": "13"}
        ]
    }"""

    with patch("builtins.open", mock_open(read_data=mock_json_content)):
        competitions = server.load_competitions()

        assert isinstance(competitions, list)
        assert len(competitions) == 2
        assert competitions[0] == {"name": "Spring Festival", "date": "2026-03-27 10:00:00", "numberOfPlaces": "25"}
        assert competitions[0]["name"] == "Spring Festival"
        assert competitions[1]["numberOfPlaces"] == "13"
