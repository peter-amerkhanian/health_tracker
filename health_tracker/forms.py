from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, Email, ValidationError


class HealthForm(FlaskForm):
    hours_of_sleep = IntegerField('Hours of sleep',
                       validators=[DataRequired()],
                       render_kw={"placeholder": ""})
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
    exercise = RadioField('Minutes of exercise',
                          choices=[("0", "0"),
                                   ("15", "15"),
                                   ("30", "30"),
                                   ("45", "45"),
                                   ("60", "60")],
                          validators=[DataRequired()])
    meditation = RadioField('Did you meditate today?',
                                    choices=[('yes','Yes'),
                                             ('no','No')],
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
                          validators=[DataRequired()])

    submit = SubmitField('Submit')