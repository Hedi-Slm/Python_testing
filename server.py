import json
from flask import Flask, render_template, request, redirect, flash, url_for, session
from datetime import datetime


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


def is_past_competition_func(competition_date):
    comp_date = datetime.strptime(competition_date, "%Y-%m-%d %H:%M:%S")
    current_date = datetime.now()
    return comp_date <= current_date


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    club = [club for club in clubs if club['email'] == request.form['email']]
    if not club:
        flash("Sorry, that email wasn't found.")
        return render_template('index.html')
    else:
        session['club_email'] = request.form['email']

    return render_template('welcome.html', club=club[0], competitions=competitions,
                           is_past_competition=is_past_competition_func)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if found_club and found_competition:
        if is_past_competition_func(found_competition['date']):
            flash("Cannot book places for past competitions")
            return render_template('welcome.html', club=club, competitions=competitions)
        else:
            return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


def can_book_places(club, competition, places_requested):
    if is_past_competition_func(competition['date']):
        return False, "Cannot book places for past competitions"
    if places_requested < 1 or places_requested > 12:
        return False, "Must book between 1 and 12 places"
    if places_requested > int(competition['numberOfPlaces']):
        return False, "Not enough places available"
    if places_requested > int(club['points']):
        return False, "Not enough points"
    return True, "Booking allowed"


def deduct_places(club, competition, places):
    competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - places)
    club['points'] = str(int(club['points']) - places)


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])

    valid, message = can_book_places(club, competition, places_required)

    if not valid:
        flash(message)
        return render_template('booking.html', club=club, competition=competition)

    deduct_places(club, competition, places_required)
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions,
                           is_past_competition=is_past_competition_func)


# TODO: Add route for points display

@app.route('/points')
def points():
    return render_template('points.html', clubs=clubs)


@app.route('/dashboard')
def dashboard():
    if 'club_email' in session:
        club = [club for club in clubs if club['email'] == session['club_email']][0]
        return render_template('welcome.html', club=club, competitions=competitions,
                               is_past_competition=is_past_competition_func)
    else:
        flash("Please log in first")
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
