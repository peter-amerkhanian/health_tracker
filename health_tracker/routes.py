from flask import render_template
from health_tracker.forms import HealthForm
from health_tracker import app, db
from health_tracker.models import Entry
import datetime


@app.route('/', methods=['post', 'get'])
def home():
    form = HealthForm()
    if form.validate_on_submit():
        entry = Entry(hours_of_sleep=form.hours_of_sleep.data,
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
        return render_template('thank_you.html')
    else:
        return render_template('index.html', form=form)


@app.route('/data')
def data():
    return render_template('data.html')