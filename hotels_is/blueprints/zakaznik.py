from flask import Blueprint, render_template
from flask_login import current_user
from werkzeug.utils import redirect
from flask.helpers import url_for

from hotels_is.models import *

zakaznik = Blueprint('zakaznik', __name__,
                     template_folder='templates')


# show user's reservations
@zakaznik.route('/my_reservations', methods=['GET'])
def my_reservations():
    if not current_user.is_anonymous:
        reservations = Rezervace.query.filter_by(id_uzivatel=current_user.id)
        return render_template('zakaznik/reservations.html', reservations=reservations)
    else:
        return render_template('error.html', error_code=401, error_message="Ke správě mých rezervací mají přístup pouze registrovaní uživatelé a presonál!")

# show profile page
@zakaznik.route('/profile', methods=['GET'])
def profile():
    if not current_user.is_anonymous:
        return render_template('zakaznik/profile.html')
    else:
        return render_template('error.html', error_code=401, error_message="Ke správě profilu mají přístup pouze registrovaní uživatelé a presonál!")