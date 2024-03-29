from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, RadioField, StringField, SelectField, DateField, PasswordField, \
    BooleanField
from wtforms.validators import DataRequired, ValidationError, length, EqualTo
from .models import Entry, User
from datetime import datetime


class HealthForm(FlaskForm):
    # def validate_unique(self, date):
    #     date_entry = date.data
    #     date = Entry.query.filter_by(date=datetime(date_entry.year, date_entry.month, date_entry.day)).first()
    #     print(date)
    #     if date is not None:
    #         raise ValidationError('That date already has an entry')

    def validate_sleep(self, field):
        print("sleep error")
        entry = field.data
        if int(entry) >= 24:
            raise ValidationError('Cannot enter 24 hours or more')

    date = DateField('Date:', validators=[DataRequired()])
    hours_of_sleep = IntegerField('Hours of sleep',
                                  validators=[DataRequired(message="Please enter an integer less than 24"),
                                              validate_sleep])
    rest = RadioField('How rested do you feel?',
                      choices=[("1", "1"),
                               ("2", "2"),
                               ("3", "3"),
                               ("4", "4"),
                               ("5", "5")],
                      validators=[DataRequired()])
    fatigue = RadioField('How fatigued do you feel?',
                         choices=[("1", "1"),
                                  ("2", "2"),
                                  ("3", "3"),
                                  ("4", "4"),
                                  ("5", "5")],
                         validators=[DataRequired()])
    exercise = RadioField('Minutes of exercise:',
                          choices=[("0", "0"),
                                   ("15", "15"),
                                   ("30", "30"),
                                   ("45", "45"),
                                   ("60", "60")],
                          validators=[DataRequired()])
    meditation = RadioField('Did you meditate today?',
                            choices=[('yes', 'Yes'),
                                     ('no', 'No')],
                            validators=[DataRequired()])
    stress = RadioField('Level of stress today (work)',
                        choices=[("1", "1"),
                                 ("2", "2"),
                                 ("3", "3"),
                                 ("4", "4"),
                                 ("5", "5")],
                        validators=[DataRequired()])
    emotion = RadioField('General emotional state',
                         choices=[("1", "1"),
                                  ("2", "2"),
                                  ("3", "3"),
                                  ("4", "4"),
                                  ("5", "5")],
                         validators=[DataRequired()])
    comfort = RadioField('General level of pain/discomfort',
                         choices=[("1", "1"),
                                  ("2", "2"),
                                  ("3", "3"),
                                  ("4", "4"),
                                  ("5", "5")],
                         validators=[DataRequired()])
    arousal = RadioField('General level of arousal',
                         choices=[("1", "1"),
                                  ("2", "2"),
                                  ("3", "3"),
                                  ("4", "4"),
                                  ("5", "5")],
                         validators=[DataRequired()], )
    headache = RadioField('Headache today?',
                          choices=[('yes', 'Yes'),
                                   ('no', 'No')],
                          validators=[DataRequired()])
    cannabis = RadioField('Cannabis use today?',
                          choices=[('yes', 'Yes'),
                                   ('no', 'No')],
                          validators=[DataRequired()])
    morning = SelectField("Morning started with:",
                          choices=[(0, '--Select One--'),
                                   ('looking at phone', 'phone'),
                                   ('exercise', 'exercise'),
                                   ('meditation', 'meditation'),
                                   ('work', 'work'),
                                   ('breakfast', 'breakfast')],
                          validators=[DataRequired()])
    pills = SelectField("Pills taken:",
                        choices=[
                            (0, '--Select One--'),
                            ('none', 'none'),
                            ('Xanax', 'Xanax'),
                            ('painkiller', 'painkiller'),
                            ('sleeping pill', 'sleeping pill')],
                        validators=[DataRequired()])
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    name = StringField('Your first name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user is not None:
            raise ValidationError("Name is already in use.")


class LoginForm(FlaskForm):
    name = StringField('Your first name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')
