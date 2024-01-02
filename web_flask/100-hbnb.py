#!/usr/bin/python3

"""
a script that starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place

app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """
    display a HTML page like 8-index.html, done during 
    the 0x01. AirBnB clone - Web static project
    """
    states = storage.all(State)
    cities = storage.all(City)
    amenities = storage.all(Amenity)
    places = storage.all(Place)

    return render_template(
            '100-hbnb.html', states=states,
            cities=cities, amenities=amenities,
            places=places
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
