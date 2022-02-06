from flask import Blueprint, render_template
from flask.helpers import url_for
from flask_login import current_user
from werkzeug.utils import redirect

from hotels_is.queries import *

vlastnik = Blueprint('vlastnik', __name__,
                     template_folder='templates')


# show hotel management site
@vlastnik.route('/hotels', methods=['GET'])
def hotels_management():
    if not current_user.is_anonymous and (current_user.role == "Admin" or current_user.role == "Vlastník"):
        hotels = get_hotels_from_database()
        if current_user.role == "Vlastník":
            my_hotels = []
            for hotel in hotels:
                for vlastnik in hotel.vlastnici:
                    if vlastnik.id == current_user.id:
                        my_hotels.append(hotel)
            return render_template('vlastnik/hotel_management.html', hotels=my_hotels)

        return render_template('vlastnik/hotel_management.html', hotels=hotels)
    else:
        return render_template('error.html', error_code=401, error_message="Neoprávněná přístup ke správě hotelů!")


@vlastnik.route('/rooms', methods=['GET'])
def rooms_management():
    if not current_user.is_anonymous and (current_user.role == "Admin" or current_user.role == "Vlastník"):
        hotels = get_hotels_from_database()
        obrazky = Obrazek.query.all()
        rooms = []
        if current_user.role == "Vlastník":
            for hotel in hotels:
                for vlastnik_local in hotel.vlastnici:
                    if vlastnik_local.id == current_user.id:
                        all_rooms = Pokoj.query.filter_by(hotel_id=hotel.id)
                        all_rooms = all_rooms.all()
                        for room in all_rooms:
                            rooms.append(room)

            return render_template('vlastnik/rooms_management.html', rooms=rooms, obrazky=obrazky, hotels=hotels)

        rooms = Pokoj.query.all()
        return render_template('vlastnik/rooms_management.html', rooms=rooms, obrazky=obrazky, hotels=hotels)
    else:
        return render_template('error.html', error_code=401, error_message="Neoprávněná přístup ke správě pokojů!")
