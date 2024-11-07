document.addEventListener('DOMContentLoaded', function() {
    let calendarEl = document.getElementById('calendar');
    let calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        editable: true,
        selectable: true,
        events: '/events',  // GET request to load events

        dateClick: function(info) {
            let title = prompt('Enter Event Title:');
            if (title) {
                let event = {
                    title: title,
                    start: info.dateStr,
                    end: info.dateStr,
                    description: ''
                };
                fetch('/events', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(event)
                }).then(response => response.json())
                  .then(data => {
                      calendar.addEvent(data);
                      alert('Event added!');
                  });
            }
        },
        eventClick: function(info) {
            if (confirm('Are you sure you want to delete this event?')) {
                fetch(`/events/${info.event.id}`, {
                    method: 'DELETE'
                }).then(response => {
                    if (response.ok) {
                        info.event.remove();
                        alert('Event deleted!');
                    }
                });
            }
        },
        eventDrop: function(info) {
            let updatedEvent = {
                id: info.event.id,
                title: info.event.title,
                start: info.event.start.toISOString(),
                end: info.event.end ? info.event.end.toISOString() : null,
                description: info.event.extendedProps.description
            };
            fetch(`/events/${info.event.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(updatedEvent)
            }).then(response => response.json())
              .then(data => {
                  alert('Event updated!');
              });
        }
    });
    calendar.render();
});
