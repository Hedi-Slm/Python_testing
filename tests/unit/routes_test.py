import pytest
from server import app
import html


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess.clear()  # ensure session is clean
        yield client


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"GUDLFT Registration Portal" in response.data


def test_show_summary_valid_email(client):
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data
    assert b"Points available: 13" in response.data


def test_show_summary_invalid_email(client):
    response = client.post("/showSummary", data={"email": "invalid@email.com"})
    decoded_response = html.unescape(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert "Sorry, that email wasn't found." in decoded_response


def test_book_future_competition(client):
    response = client.get("/book/Spring%20Festival/Simply%20Lift")
    assert response.status_code == 200
    assert b"Spring Festival" in response.data
    assert b"Places available: 25" in response.data


def test_book_past_competition(client):
    response = client.get("/book/Fall%20Classic/Simply%20Lift")
    assert response.status_code == 200
    assert b"Cannot book places for past competitions" in response.data


def test_book_invalid_club(client):
    response = client.get("/book/Spring%20Festival/Invalid%20Club")
    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data


def test_book_invalid_competition(client):
    response = client.get("/book/Invalid%20Competition/Simply%20Lift")
    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data


def test_purchase_valid_places(client):
    response = client.post("/purchasePlaces", data={
        "club": "Simply Lift",
        "competition": "Spring Festival",
        "places": "4"
    })
    assert response.status_code == 200
    assert b"Great, booking complete!" in response.data


def test_purchase_invalid_places(client):
    response = client.post("/purchasePlaces", data={
        "club": "Simply Lift",
        "competition": "Spring Festival",
        "places": "20"
    })
    assert response.status_code == 200
    assert b"Must book between 1 and 12 places" in response.data


def test_points_page(client):
    response = client.get("/points")
    assert response.status_code == 200
    assert b"Simply Lift" in response.data  # club name appears


def test_dashboard_with_login(client):
    with client.session_transaction() as sess:
        sess['club_email'] = "john@simplylift.co"
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data


def test_dashboard_without_login(client):
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in first" in response.data


def test_logout(client):
    with client.session_transaction() as sess:
        sess['club_email'] = "john@simplylift.co"
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"GUDLFT Registration Portal" in response.data