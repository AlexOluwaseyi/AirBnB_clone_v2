#!/usr/bin/python3

"""
a script that starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def state_list():
    """
    Display a HTML page with a list of all State objects sorted by name.
    """
    states = storage.all(State)
    # sorted_states = sorted(states, key=lambda x: x.name)

    return render_template('7-states_list.html', states=states)


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
