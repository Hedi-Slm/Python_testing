import pytest
from server import can_book_places, deduct_places


@pytest.fixture
def club():
    return {"name": "Test Club", "email": "test@club.com", "points": "15"}


@pytest.fixture
def future_competition():
    return {"name": "Future Event", "date": "2099-12-31 12:00:00", "numberOfPlaces": "20"}


@pytest.fixture
def past_competition():
    return {"name": "Past Event", "date": "2000-01-01 12:00:00", "numberOfPlaces": "20"}


# ----------- can_book_places Tests -----------


class TestCanBookPlaces:
    def test_cannot_book_past_competition(self, club, past_competition):
        valid, message = can_book_places(club, past_competition, 5)
        assert not valid
        assert message == "Cannot book places for past competitions"

    def test_cannot_book_less_than_1_place(self, club, future_competition):
        valid, message = can_book_places(club, future_competition, 0)
        assert not valid
        assert message == "Must book between 1 and 12 places"

    def test_cannot_book_more_than_12_places(self, club, future_competition):
        valid, message = can_book_places(club, future_competition, 13)
        assert not valid
        assert message == "Must book between 1 and 12 places"

    def test_cannot_book_more_places_than_available(self, club, future_competition):
        # Set competition places to 9 and ask for 10
        future_competition['numberOfPlaces'] = "9"
        valid, message = can_book_places(club, future_competition, 10)
        assert not valid
        assert message == "Not enough places available"

    def test_cannot_book_more_places_than_points(self, club, future_competition):
        # Set club points to 5 and ask for 8
        club['points'] = "5"
        valid, message = can_book_places(club, future_competition, 8)
        assert not valid
        assert message == "Not enough points"

    def test_can_book_valid_request(self, club, future_competition):
        valid, message = can_book_places(club, future_competition, 5)
        assert valid
        assert message == "Booking allowed"

    def test_can_book_exactly_12(self, club, future_competition):
        valid, message = can_book_places(club, future_competition, 12)
        assert valid
        assert message == "Booking allowed"

    def test_can_book_exactly_number_of_points(self, club, future_competition):
        # Set club points to 10 and ask for 10
        club['points'] = "10"
        valid, message = can_book_places(club, future_competition, 10)
        assert valid
        assert message == "Booking allowed"

    def test_can_book_exactly_number_of_places_available(self, club, future_competition):
        # Set competition places to 10 and ask for 10
        future_competition['numberOfPlaces'] = "10"
        valid, message = can_book_places(club, future_competition, 10)
        assert valid
        assert message == "Booking allowed"


# ----------- deduct_places Tests -----------


class TestDeductPlaces:
    def test_deduct_places_correctly(self, club, future_competition):
        # Club points = 15; competition slots = 20
        deduct_places(club, future_competition, 5)

        assert club['points'] == "10"
        assert future_competition['numberOfPlaces'] == "15"
