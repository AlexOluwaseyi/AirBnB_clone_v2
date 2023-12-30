#!/usr/bin/python3

"""
a script that starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_states():
    """
    Display a HTML page with a list of all State objects sorted by name.
    """
    states = storage.all(State)
    # cities = storage.all(City)
    # sorted_states = sorted(states, key=lambda x: x.name)

    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown(exception):
    """
    Remove the current SQLAlchemy Session after each request.
    """
    storage.close()


if __name__ == '__main__':
    """
    Your web application must be listening on 0.0.0.0, port 5000
    """
    app.run(host='0.0.0.0', port=5000)
