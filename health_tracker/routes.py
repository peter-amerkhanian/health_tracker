from flask import render_template, session, url_for, redirect
from health_tracker import app, db
from health_tracker.forms import HealthForm, LoginForm
from health_tracker.models import Entry
from health_tracker.graphics import Graph
import datetime


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
                      hours_of_sleep=form.hours_of_sleep.data,
                      rest=form.rest.data,
                      fatigue=form.fatigue.data,
                      exercise=form.exercise.data,
                      meditation=form.meditation.data,
                      stress=form.stress.data,
                      emotion=form.emotion.data,
                      comfort=form.comfort.data,
                      arousal=form.arousal.data,
                      date=datetime.datetime.today()
                      )
        db.session.add(entry)
        db.session.commit()
        return render_template('thank_you.html', name=name.title())
    else:
        return render_template('survey.html', name=name.title(), form=form)


@app.route('/data')
def data():
    name = session.get('name')
    if not name:
        session['logout_alert'] = True
        return redirect(url_for('survey'))
    graph = Graph(name)
    graph.get_data_sqlite(sessions_name=name)
    graph_data, graph_data_2 = graph.pygal_line_plot()
    return render_template('data.html', graph_data=graph_data, graph_data_2=graph_data_2, graph=graph)