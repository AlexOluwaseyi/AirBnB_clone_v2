#!/usr/bin/python3

"""
a script that starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """
    Display a HTML page with a list of all State objects sorted by name.
    """
    states = storage.all(State)
    return render_template('9-states.html', states=states, state_id="None")


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """
    Display a HTML page with a list of all State objects sorted by name.
    """
    states = storage.all(State)
    selected_state = None

    for state in states.values():
        if state.id == id:
            selected_state = state
            break

    return render_template(
            '9-states.html', states=states,
            selected_state=selected_state, state_id=id
            )


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
