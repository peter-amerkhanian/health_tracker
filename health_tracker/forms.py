from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, RadioField, StringField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, ValidationError


class HealthForm(FlaskForm):

    def validate_scroll(form, field):
        if field.data == 0:
            raise ValidationError('Please fill out all fields')

    date = DateField('Date:', validators=[DataRequired()])
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
                          validators=[DataRequired(), validate_scroll])
    pills = SelectField("Pills taken:",
                        choices=[
                            (0, '--Select One--'),
                            ('none', 'none'),
                            ('Xanax', 'Xanax'),
                            ('painkiller', 'painkiller'),
                            ('sleeping pill', 'sleeping pill')],
                        validators=[DataRequired(), validate_scroll])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    def validate_name(form, field):
        if field.data.lower() not in ['peter', 'tate', 'zarlasht', 'test']:
            raise ValidationError('Sorry, you do not have an account with health tracker.')
    name = StringField('Your first name', validators=[DataRequired(), validate_name])
    submit = SubmitField('Submit')
