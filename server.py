import json
from flask import Flask, render_template, request, redirect, flash, url_for, session
from datetime import datetime


def is_past_competition_func(competition_date):
    comp_date = datetime.strptime(competition_date, "%Y-%m-%d %H:%M:%S")
    current_date = datetime.now()
    return comp_date < current_date


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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    club = [club for club in clubs if club['email'] == request.form['email']]
    if not club:
        flash("Sorry, that email wasn't found.")
        return render_template('index.html')
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


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    club_points = int(club['points'])

    if is_past_competition_func(competition['date']):
        flash("Cannot book places for past competitions")
        return render_template('welcome.html', club=club, competitions=competitions,
                               is_past_competition=is_past_competition_func)

    places_required = int(request.form['places'])
    competition_places = int(competition['numberOfPlaces'])

    if places_required > competition_places:
        flash('Not enough places-please try again')
        return render_template('booking.html', club=club, competition=competition,
                               is_past_competition=is_past_competition_func)

    if 12 < places_required < 1:
        flash('Cannot book less than 1 or more than 12 places')
        return render_template('booking.html', club=club, competition=competition,
                               is_past_competition=is_past_competition_func)
    if places_required > club_points:
        flash('Not enough points-please try again')
        return render_template('booking.html', club=club, competition=competition,
                               is_past_competition=is_past_competition_func)
    competition['numberOfPlaces'] = competition_places - places_required
    club['points'] = club_points - places_required
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
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash("Please log in first")
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
