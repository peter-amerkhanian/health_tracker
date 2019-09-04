from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, RadioField, StringField, SelectField, DateTimeField, DateField
from wtforms.validators import DataRequired, ValidationError
from .models import Entry
from datetime import datetime


class HealthForm(FlaskForm):
    def validate_unique(self, field):
        date_entry = field.data
        date = Entry.query.filter_by(date=datetime(date_entry.year, date_entry.month, date_entry.day)).first()
        print('doin it')
        if date is not None:
            print("error")
            raise ValidationError('That date already has an entry')

    date = DateField('Date:', validators=[DataRequired(), validate_unique])
    hours_of_sleep = IntegerField('Hours of sleep',
                                  validators=[DataRequired()])
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
                          validators=[DataRequired(message="Please do not leave fields blank")])
    pills = SelectField("Pills taken:",
                        choices=[
                            (0, '--Select One--'),
                            ('none', 'none'),
                            ('Xanax', 'Xanax'),
                            ('painkiller', 'painkiller'),
                            ('sleeping pill', 'sleeping pill')],
                        validators=[DataRequired(message="Please do not leave fields blank")])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    def validate_name(form, field):
        if field.data.lower() not in ['peter', 'tate', 'zarlasht', 'test']:
            raise ValidationError('Sorry, you do not have an account with health tracker.')
    name = StringField('Your first name', validators=[DataRequired(), validate_name])
    submit = SubmitField('Submit')
