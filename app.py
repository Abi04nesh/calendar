from flask import Flask, jsonify, request, render_template
from models import db, Event
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Initialize the database
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

if __name__ == '__main__':
    app.run(debug=True)
