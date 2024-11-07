from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start = db.Column(db.String(100), nullable=False)  # ISO format date-time
    end = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'start': self.start,
            'end': self.end,
            'description': self.description
        }
