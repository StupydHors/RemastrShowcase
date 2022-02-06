from flask import Blueprint, render_template, jsonify
from flask.helpers import url_for
from flask_login import current_user
from werkzeug.utils import redirect

from hotels_is.models import *
from hotels_is.queries import get_hotels_from_database

recepcni = Blueprint('recepcni', __name__,
                     template_folder='templates')


# show user management site
@recepcni.route('/reservations', methods=['GET'])
def reservations_management():
    if not current_user.is_anonymous and (
            current_user.role == "Admin" or current_user.role == "Recepční" or current_user.role == "Vlastník"):
        hotels = []
        uzivatele = Uzivatel.query.all()
        pokoje = Pokoj.query.all()

        if current_user.role == "Recepční":
            recepcni_hotel = Recepcni.query.filter_by(recepcni_id=current_user.id)
            recepcni_hotel = recepcni_hotel.first()
            if recepcni_hotel is None:
                reservations = None
                return render_template('recepcni/reservations_management.html', reservations=reservations,
                                       hotels=hotels, uzivatele=uzivatele)
            reservations = Rezervace.query.filter_by(id_hotel=recepcni_hotel.hotel_id)
            hotels = Hotel.query.filter_by(id=recepcni_hotel.hotel_id).all()
        elif current_user.role == "Vlastník":
            vlastnik_hotel = Vlastnik.query.filter_by(vlastnik_id=current_user.id)
            vlastnik_hotel = vlastnik_hotel.first()
            if vlastnik_hotel is None:
                reservations = None
                return render_template('recepcni/reservations_management.html', reservations=reservations,
                                       hotels=hotels, uzivatele=uzivatele)
            hotels = Hotel.query.filter_by(id=vlastnik_hotel.hotel_id).all()
            reservations = Rezervace.query.filter_by(id_hotel=vlastnik_hotel.hotel_id)
        else:
            hotels = get_hotels_from_database()
            reservations = Rezervace.query.all()

        return render_template('recepcni/reservations_management.html', reservations=reservations, hotels=hotels,
                               uzivatele=uzivatele, pokoje=pokoje)
    else:
        return render_template('error.html', error_code=401, error_message="Neoprávěný přístup ke správě rezervací!")


@recepcni.route('/get_pokoj/<string:entity>/<int:reservation>', methods=['GET'])
def get_pokoj(entity, reservation):
    if not current_user.is_anonymous and (
            current_user.role == "Admin" or current_user.role == "Recepční" or current_user.role == "Vlastník"):
        if entity == "rezervace":
            rezervace = Rezervace.query.filter_by(id=reservation).first()
            pokoj = Pokoj.query.filter_by(id=rezervace.id_pokoj).first()
            odpoved = {'cena': pokoj.cena_za_noc}
            return jsonify(odpoved)
        elif entity == "pokoj":
            pokoj = Pokoj.query.filter_by(id=reservation).first()
            odpoved = {'cena': pokoj.cena_za_noc}
            return jsonify(odpoved)
    else:
        return render_template('error.html', error_code=401, error_message="Neoprávěný přístup ke správě rezervací!")


@recepcni.route('/get_rooms/<int:hotel>', methods=['GET'])
def get_rooms(hotel):
    if not current_user.is_anonymous and (current_user.role == "Admin" or current_user.role == "Recepční" or current_user.role == "Vlastník"):
        odpoved = []
        pokoje = Pokoj.query.filter_by(hotel_id=hotel).all()
        for pokoj in pokoje:
            odpoved.append([pokoj.id, pokoj.cislo])
        return jsonify(odpoved)
    
    else:
        return render_template('error.html', error_code=401, error_message="Neoprávěný přístup ke správě rezervací!")
