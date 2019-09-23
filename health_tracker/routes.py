from flask import render_template, session, url_for, redirect, send_from_directory, request, flash
from health_tracker import app, db
from health_tracker.forms import HealthForm, LoginForm, RegistrationForm
from health_tracker.models import Entry, User
from health_tracker.graphics import UserData
from datetime import datetime
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
import os


@app.route('/', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('survey'))
    form = LoginForm()
    if form.validate_on_submit():
        print(form.data)
        user = User.query.filter_by(name=form.name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid name or password", 'error')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('survey')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup', methods=['post', 'get'])
def sign_up():
    sign_up_form = RegistrationForm()
    if sign_up_form.validate_on_submit():
        print('ok')
        user = User(name=sign_up_form.name.data, password_hash="null")
        user.set_password(sign_up_form.password.data)
        print(user)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful.", 'info')
        print(sign_up_form.data)
        return redirect(url_for('login'))
    return render_template('sign_up.html', sign_up=sign_up_form)


@app.route('/survey', methods=['post', 'get'])
@login_required
def survey():
    name = current_user.name
    form = HealthForm()
    if request.method == 'POST' and form.validate():
        date_entry = form.date.data
        entry = Entry(name=name,
                      date=datetime(date_entry.year, date_entry.month, date_entry.day),
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
        return render_template('survey.html', name=name.title(), form=form)


@app.route('/data')
@login_required
def data():
    name = current_user.name
    user = UserData(name)
    user.get_data_sqlite()
    csv_file = '{}_data_{}.csv'.format(name, datetime.today().strftime("%Y"))
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
@login_required
def visuals():
    name = current_user.name
    path = url_for('static', filename='{}_line_graph.svg'.format(name))
    return render_template('visuals.html', path=path)


@app.route('/download_csv')
@login_required
def download_csv():
    name = current_user.name
    file = '{}_data_{}.csv'.format(name, datetime.today().strftime("%Y"))
    if os.getcwd().endswith('health_tracker'):
        path = os.path.join(os.getcwd(), 'health_tracker', 'uploads')
    else:
        path = os.path.join(os.getcwd(), 'health_tracker', 'health_tracker', 'uploads')
    return send_from_directory(path, file, as_attachment=True)


@app.route('/download_xlsx')
@login_required
def download_xlsx():
    name = current_user.name
    file = '{}_data_{}.xlsx'.format(name, datetime.today().strftime("%Y"))
    if os.getcwd().endswith('health_tracker'):
        path = os.path.join(os.getcwd(), 'health_tracker', 'uploads')
    else:
        path = os.path.join(os.getcwd(), 'health_tracker', 'health_tracker', 'uploads')
    return send_from_directory(path, file, as_attachment=True)


@app.route('/table')
@login_required
def table():
    name = current_user.name
    user = UserData(name)
    user.get_data_sqlite()
    user.pandas_df
    html = user.build_table()
    return render_template('table.html', html=html)
