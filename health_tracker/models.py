from health_tracker import db


class Entry(db.Model):
    __tablename__ = "entry"
    name = db.Column(db.String(50), unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    hours_of_sleep = db.Column(db.Integer, unique=False, nullable=True)
    rest = db.Column(db.Integer, unique=False, nullable=True)
    fatigue = db.Column(db.Integer, unique=False, nullable=True)
    exercise = db.Column(db.Integer, unique=False, nullable=True)
    meditation = db.Column(db.String(10), unique=False, nullable=True)
    stress = db.Column(db.Integer, unique=False, nullable=True)
    emotion = db.Column(db.Integer, unique=False, nullable=True)
    comfort = db.Column(db.Integer, unique=False, nullable=True)
    arousal = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return "Entrys('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(self.hours_of_sleep,
                                                                                          self.rest,
                                                                                          self.fatigue,
                                                                                          self.exercise,
                                                                                          self.meditation,
                                                                                          self.stress,
                                                                                          self.emotion,
                                                                                          self.arousal,
                                                                                          self.date)
