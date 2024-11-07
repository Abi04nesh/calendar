from flask import Flask, jsonify, request, render_template
from models import db, Event
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events])

@app.route('/events', methods=['POST'])
def add_event():
    data = request.json
    # Check if the event already exists (same start time and title)
    existing_event = Event.query.filter_by(start=data['start'], title=data['title']).first()
    if existing_event:
        return jsonify({'message': 'Event already exists'}), 400  # Return an error if duplicate

    new_event = Event(
        title=data['title'],
        start=data['start'],
        end=data['end'],
        description=data.get('description', '')
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event.to_dict()), 201


@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Event deleted'}), 200
    return jsonify({'message': 'Event not found'}), 404

@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event = Event.query.get(event_id)
    if event:
        data = request.json
        event.title = data['title']
        event.start = data['start']
        event.end = data['end']
        event.description = data.get('description', '')
        db.session.commit()
        return jsonify(event.to_dict())
    return jsonify({'message': 'Event not found'}), 404
