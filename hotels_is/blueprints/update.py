from flask import Blueprint, render_template, flash
import flask
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask_login import current_user

from hotels_is.blueprints.create import create_vlastnik
from hotels_is.blueprints.delete import delete_vlastnik
from hotels_is.queries import *
from hotels_is.utils.json_creator import *
from hotels_is.utils.passwords import hash_password, verify_password

import datetime
import time

update = Blueprint('update', __name__,
                   template_folder='templates')


@update.route('/<string:entity>/<int:id>', methods=['POST'])
def update_page(entity, id):
    if entity == "uzivatel":
        if not current_user.is_anonymous and current_user.role == "Admin":
            uzivatel = Uzivatel.query.get_or_404(id)
            uzivatel.email = request.form['email']
            if request.form['password'] != "":
                uzivatel.password = hash_password(request.form['password'])
            uzivatel.role = request.form['role']

            if request.form.get('hotel'):  # hotel???
                if uzivatel.role == "Vlastník":  # přidávání vlastníka??? toto by zde asi nemělo být
                    vlastnik = Vlastnik(vlastnik_id=uzivatel.id, hotel_id=int(request.form['hotel']))
                    db.session.add(vlastnik)
                elif uzivatel.role == "Recepční":
                    recepcni = Recepcni(recepcni_id=uzivatel.id, hotel_id=int(request.form['hotel']))
                    db.session.add(recepcni)
            try:
                db.session.commit()
            except:
                return render_template('error.html', error_code=500, error_message="Při snaze upravit uživatele došlo k chybě!")
        else:
            return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")

    elif entity == "pokoj":
        if not current_user.is_anonymous and (current_user.role == "Admin" or current_user.role == "Vlastník"):
            pokoj = Pokoj.query.get_or_404(id)
            pokoj.cena_za_noc = int(request.form['cena_za_noc'])
            pokoj.pocet_luzek = int(request.form['pocet_luzek'])
            pokoj.typ = request.form['typ']
            pokoj.velikost = request.form['velikost']
            if request.form['vyber_obrazku'] != 'bez_zmeny':
                if request.form['vyber_obrazku'] == 'odebrat':
                    pokoj.fotka_id = None
                else:
                    pokoj.fotka_id = request.form['vyber_obrazku']
            pokoj.klimatizace = True if request.form.get('klimatizace') else False
            pokoj.balkon = True if request.form.get('balkon') else False
            pokoj.pristylka = True if request.form.get('pristylka') else False
            try:
                db.session.commit()
            except:
                return render_template('error.html', error_code=500, error_message="Při snaze upravit pokoj došlo k chybě!")
        else:
            return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")

    elif entity == "rezervace":
        if not current_user.is_anonymous and (current_user.role == "Admin" or current_user.role == "Vlastník" or current_user.role == "Recepční"):
            rez = Rezervace.query.get_or_404(id)
            datumZ = time.strptime(request.form['datum_zacatek'], "%Y-%m-%d")
            rez.datum_zacatek = datetime.datetime(datumZ.tm_year, datumZ.tm_mon, datumZ.tm_mday)
            datumK = time.strptime(request.form['datum_konec'], "%Y-%m-%d")
            rez.datum_konec = datetime.datetime(datumK.tm_year, datumK.tm_mon, datumK.tm_mday)
            rez.zaplaceno = True if request.form.get('zaplaceno') else False
            rez.check_in = True if request.form.get('check_in') else False
            rez.finalni_cena = int(request.form['finalni_cena'])
            try:
                db.session.commit()
            except Exception as e:
                # print(e)
                return render_template('error.html', error_code=500, error_message="Při snaze upravit rezervaci došlo k chybě!")
        else:
            return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")

    return redirect(request.referrer)


@update.route('/hotel/<int:id>', methods=['POST'])
def update_hotel(id):
    if not current_user.is_anonymous and (current_user.role == "Admin" or current_user.role == "Vlastník"):
        hotel = Hotel.query.get_or_404(id)
        hotel.name = request.form['name_hotel']
        hotel.address = request.form['address_hotel']
        hotel.rating = request.form['rating_hotel']
        try:
            db.session.commit()
        except:
            return render_template('error.html', error_code=500, error_message="Při snaze upravit hotel došlo k chybě!")

        return redirect(request.referrer)
    else:
        return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")

@update.route('/vlastnik/<int:vlastnik_id>', methods=['POST'])
def update_vlastnik(vlastnik_id):
    if not current_user.is_anonymous and (current_user.role == "Admin"):
        for hotel in get_hotels_from_database():
            vlastnik = Vlastnik.query.filter_by(vlastnik_id=vlastnik_id, hotel_id=hotel.id).first()
            if request.form.get(hotel.name):
                # hotel vlastníme a nebo by jsme měli začít
                if vlastnik is None:
                    # Teprve začneme vlastnit
                    create_vlastnik(vlastnik_id, hotel.id)
                else:
                    # již vlastníme a měly bychom v tom pokračovat -> netřeba nic dělat
                    pass
            else:
                # hotel nevlastníme a nebo bychom měli přestat
                if vlastnik is None:
                    # Nevlastníme a vlastnit nemáme -> netřeba nic dělat
                    pass
                else:
                    # již vlastníme a měly bychom v tom pokračovat -> netřeba nic dělat
                    delete_vlastnik(vlastnik_id, hotel.id)
        return redirect(url_for("admin.dashboard"))
    else:
        return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")


@update.route('/rezervace/<int:idcko>/<string:operace>', methods=['GET'])
def update_rezervace_check_in(idcko, operace):
    if not current_user.is_anonymous and\
            (current_user.role == "Admin" or current_user.role == "Vlastník" or current_user.role == "Recepční"):
        rez = Rezervace.query.get_or_404(idcko)
        if operace == "check-in":
            rez.check_in = True
        elif operace == "check-out":
            rez.check_out = True
        elif operace == "platba-provedena":
            rez.zaplaceno = True
        elif operace == "rezervace-potvrzena":
            rez.potvrzeno = True
        else:
            return render_template('error.html', error_code=500,
                                   error_message="Při snaze upravit rezeraci došlo k chybě!")

        try:
            db.session.commit()
        except:
            return render_template('error.html', error_code=500,
                                   error_message="Při snaze upravit rezeraci došlo k chybě!")

        return redirect(request.referrer)
    else:
        return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")

@update.route('/profile', methods=['POST'])
def update_profile():
    if not current_user.is_anonymous:
        uzivatel = Uzivatel.query.get(current_user.id)
        uzivatel.name = request.form['name']
        uzivatel.phone_number = request.form['phone_number']
        try:
            db.session.commit()
            flash("Údaje byly úspěšně změněny.")
        except:
            return render_template('error.html', error_code=500, error_message="Při snaze upravit profil došlo k chybě!")
        return redirect(request.referrer)

    else:
        return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")

@update.route('/password', methods=['POST'])
def update_password():
    if not current_user.is_anonymous:
        uzivatel = Uzivatel.query.get(current_user.id)
        # check old password
        if verify_password(current_user.password, request.form['old_password']):
            # check password check
            if request.form['new_password'] ==  request.form['new_password_check']:
                uzivatel.password = hash_password(request.form['new_password'])
                try:
                    db.session.commit()
                    flash('Heslo bylo úspěšně změněno.')
                except:
                    return render_template('error.html', error_code=500, error_message="Při snaze upravit heslo došlo k chybě!")
            else:
                flash('Kontrola nového hesla nesedí se zadaným novým heslem.')
                flash("Požadavek se nezdařil.")
        else:
            flash('Stará hesla se neshodují.')
            flash("Požadavek se nezdařil.")

        return redirect(request.referrer)

    else:
        return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")
