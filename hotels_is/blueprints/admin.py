from flask import Blueprint, render_template
from flask_login import current_user
from werkzeug.utils import redirect

from hotels_is.queries import *
from hotels_is.utils.json_creator import *

admin = Blueprint('admin', __name__,
                  template_folder='templates')


# show admin dashboard page
@admin.route('/', methods=['GET'])
def dashboard():
    if not current_user.is_anonymous and current_user.role == "Admin":
        users, hotels, rooms, reservations = create_tables_data()
        return render_template('admin/dashboard.html', users=users, hotels=hotels, reservations=reservations,
                               rooms=rooms)
    else:
        return render_template('error.html', error_code=401, error_message="Neoprávněný přístup k administrátorským nástrojům!")


# show user management site
@admin.route('/users', methods=['GET'])
def users_management():
    if not current_user.is_anonymous and current_user.role == "Admin":
        users = get_users_from_database()
        return render_template('admin/users_management.html', users=users, hotels=create_hotels_json())
    else:
        return render_template('error.html', error_code=401, error_message="Neoprávněný přístup k administrátorským nástrojům!")


# show owner management site
@admin.route('/owners/<string:entity>/<int:owner_id>', methods=['GET'])
def owner_management(entity, owner_id):
    if not current_user.is_anonymous and current_user.role == "Admin":
        if entity == "vlastnik":
            uzivatel = Uzivatel.query.get(int(owner_id))
            vlastnici = Vlastnik.query.all()
            vlastnim = Vlastnik.query.filter_by(vlastnik_id=int(owner_id)).all()
            hotels = get_hotels_from_database()
            vlastnena_id = []
            for vlastnen in vlastnim:
                vlastnena_id.append(vlastnen.hotel_id)

            return render_template('admin/owner_management.html', entity=entity, uzivatel=uzivatel, vlastnici=vlastnici,
                                   hotels=hotels, vlastnena_id=vlastnena_id)
    else:
        return render_template('error.html', error_code=401, error_message="Neoprávněný přístup k administrátorským nástrojům!")


def create_tables_data():
    users = Uzivatel.query.all()
    rooms = Pokoj.query.all()
    reservations = Rezervace.query.all()
    hotels = get_hotels_from_database()

    return users, hotels, rooms, reservations
