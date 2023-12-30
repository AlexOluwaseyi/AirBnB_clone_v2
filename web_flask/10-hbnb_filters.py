"""#!/usr/bin/python3"""

"""
a script that starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity

app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def states():
    """
    display a HTML page like 6-index.html, which was done
    during the project 0x01. AirBnB clone - Web static
    """
    states = storage.all(State)
    return render_template('10-hbnb_filters.html', states=states)


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
