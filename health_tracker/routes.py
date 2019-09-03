from flask import render_template, session, url_for, redirect, send_from_directory, flash, request
from health_tracker import app, db
from health_tracker.forms import HealthForm, LoginForm
from health_tracker.models import Entry
from health_tracker.graphics import UserData
import datetime
import os


@app.route('/', methods=['post', 'get'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data.lower()
        session['logout_alert'] = False
        return redirect(url_for('survey'))
    else:
        return render_template('login.html', form=form, logout_alert=session.get('logout_alert'))


@app.route('/survey', methods=['post', 'get'])
def survey():
    name = session.get('name')
    if not name:
        session['logout_alert'] = True
        return redirect(url_for('login'))
    form = HealthForm()
    if form.validate_on_submit():
        entry = Entry(name=session['name'],
                      date=form.date.data,
                      hours_of_sleep=form.hours_of_sleep.data,
                      rest=form.rest.data,
                      fatigue=form.fatigue.data,
                      exercise=form.exercise.data,
                      meditation=form.meditation.data,
                      stress=form.stress.data,
                      emotion=form.emotion.data,
                      comfort=form.comfort.data,
                      arousal=form.arousal.data,
                      headache=form.headache.data,
                      cannabis=form.cannabis.data,
                      morning=form.morning.data
                      )
        print(entry)
        db.session.add(entry)
        db.session.commit()
        return render_template('thank_you.html', name=name.title())
    else:
        flash("Error: Missing fields")
        return render_template('survey.html', name=name.title(), form=form)


@app.route('/data')
def data():
    name = session.get('name')
    if not name:
        session['logout_alert'] = True
        return redirect(url_for('login'))
    user = UserData(name)
    user.get_data_sqlite()
    csv_file = '{}_data_{}.csv'.format(name, datetime.datetime.today().strftime("%Y"))
    xlsx_file = csv_file.replace('.csv', '.xlsx')
    if os.getcwd().endswith('health_tracker'):
        path = os.path.join(os.getcwd(), 'health_tracker', 'uploads')
    else:
        path = os.path.join(os.getcwd(), 'health_tracker', 'health_tracker', 'uploads')
    user.to_csv(os.path.join(path, csv_file))
    user.to_excel(os.path.join(path, xlsx_file))
    user.pygal_line_plot(['stress', 'fatigue', 'comfort', 'arousal', 'rest'])
    return render_template('data.html', user=user)


@app.route('/visualized_data')
def visuals():
    name = session.get('name')
    if not name:
        session['logout_alert'] = True
        return redirect(url_for('login'))
    path = url_for('static', filename='{}_line_graph.svg'.format(name))
    return render_template('visuals.html', path=path)


@app.route('/download_csv')
def download_csv():
    name = session.get('name')
    if not name:
        session['logout_alert'] = True
        return redirect(url_for('login'))
    file = '{}_data_{}.csv'.format(name, datetime.datetime.today().strftime("%Y"))
    if os.getcwd().endswith('health_tracker'):
        path = os.path.join(os.getcwd(), 'health_tracker', 'uploads')
    else:
        path = os.path.join(os.getcwd(), 'health_tracker', 'health_tracker', 'uploads')
    return send_from_directory(path, file, as_attachment=True)


@app.route('/download_xlsx')
def download_xlsx():
    name = session.get('name')
    if not name:
        session['logout_alert'] = True
        return redirect(url_for('login'))
    file = '{}_data_{}.xlsx'.format(name, datetime.datetime.today().strftime("%Y"))
    if os.getcwd().endswith('health_tracker'):
        path = os.path.join(os.getcwd(), 'health_tracker', 'uploads')
    else:
        path = os.path.join(os.getcwd(), 'health_tracker', 'health_tracker', 'uploads')
    return send_from_directory(path, file, as_attachment=True)
