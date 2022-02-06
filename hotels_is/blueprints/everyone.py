from flask import Blueprint, render_template, request

from hotels_is.models import *
from hotels_is.queries import get_rooms_for_offer

everyone = Blueprint('everyone', __name__,
                     template_folder='templates')


@everyone.route('/offering', methods=['GET', 'POST'])
def offering():
    filter, hotels, rooms = get_rooms_for_offer()
    obrazky = Obrazek.query.all()
    return render_template('everyone/offering.html', rooms=rooms, hotels=hotels, filter=filter, obrazky=obrazky)


@everyone.route('/summary', methods=['GET', 'POST'])
def summary():
    result = request.form
    # získat rezervace na pokoj, zjistit jak je co obsazený 
    return render_template('everyone/new_reservation.html', result=result)


@everyone.route('/checkout', methods=['GET', 'POST'])
def checkout():
    return render_template('everyone/offering.html')
