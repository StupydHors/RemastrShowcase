from flask import Blueprint, render_template, abort, request
from flask_login import current_user
from jinja2 import TemplateNotFound
from werkzeug.utils import redirect
from flask.helpers import flash, url_for

from hotels_is.utils.json_creator import *
from hotels_is.utils.passwords import hash_password

create = Blueprint('create', __name__,
                   template_folder='templates')


@create.route('/create_<string:entity>', methods=['POST'])
def create_entity(entity):

    if entity == "uzivatel":
        if not current_user.is_anonymous and current_user.role == "Admin":
            uzivatel = Uzivatel.query.filter_by(email=request.form['email']).first()
            # test if email is already registered
            if not uzivatel:
                name = request.form['name']
                phone_number = request.form['phone_number']
                email = request.form['email']
                password = request.form['password']
                role = request.form['role']
                uzivatel = Uzivatel(email=email, password=hash_password(password), role=role, name=name,phone_number=phone_number)
                try:
                    db.session.add(uzivatel)
                    db.session.commit()
                except:
                    return render_template('error.html', error_code=500, error_message="Při vytváření uživatele došlo k chybě!")
            else:
                flash("Při vytváření uživatele došlo k chybě!")
                flash("Email je již zabraný.")

            return redirect(url_for("admin.users_management"))

        else:
            return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")


    elif entity == "hotel":
        if not current_user.is_anonymous and (current_user.role == "Admin" or current_user.role == "Vlastník"):
            name = request.form['name']
            address = request.form['address']
            rating = request.form['rating']
            hotel = Hotel(name=name, address=address, rating=rating)
            try:
                db.session.add(hotel)
                db.session.commit()
            except:
                return render_template('error.html', error_code=500, error_message="Při vytváření hotelu došlo k chybě!")
            
            if current_user.role == "Vlastník":
                my_new_hotel = Hotel.query.filter(Hotel.name == name, Hotel.address == address, Hotel.rating == rating).first()
                create_vlastnik(current_user.id, my_new_hotel.id)

            return redirect(url_for("vlastnik.hotels_management"))
        
        else:
            return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")

    elif entity == "pokoj":
        if not current_user.is_anonymous and (current_user.role == "Admin" or current_user.role == "Vlastník"):
            hotel_id = int(request.form['hotel_id'])
            cislo = int(request.form['cislo'])
            cena_za_noc = int(request.form['cena_za_noc'])
            pocet_luzek = int(request.form['pocet_luzek'])
            typ = request.form['typ']
            velikost = request.form['velikost']
            klimatizace = True if request.form.get('klimatizace') else False
            balkon = True if request.form.get('balkon') else False
            pristylka = True if request.form.get('pristylka') else False

            pokoj = Pokoj(hotel_id=hotel_id, cislo=cislo, cena_za_noc=cena_za_noc, pocet_luzek=pocet_luzek, typ=typ,
                        velikost=velikost, klimatizace=klimatizace, balkon=balkon, pristylka=pristylka)
            try:
                db.session.add(pokoj)
                db.session.commit()
            except:
                return render_template('error.html', error_code=500, error_message="Při vytváření pokoje došlo k chybě!")

            return redirect(url_for("vlastnik.rooms_management"))
        
        else:
            return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")

    elif entity == "rezervace":
        password = None
        role = None
        name = None
        phone_number = None
        if current_user.is_anonymous:
            id_uzivatel = None
            if True if request.form.get('registrace') else False:
                password = request.form['heslo']
                role = "Zákazník"
                name = request.form['name']
                phone_number = request.form['phone_number']
        else:
            id_uzivatel = int(request.form['id_uzivatel'])

        try:
            email_uzivatel = str(request.form['email_uzivatel'])
        except:
            email_uzivatel = Uzivatel.query.get(int(id_uzivatel)).email

        if current_user.is_anonymous and True if request.form.get('registrace') else False:
            uzivatel = Uzivatel(email = email_uzivatel, password=hash_password(password), role=role, name=name, phone_number=phone_number)
            try:
                db.session.add(uzivatel)
                db.session.commit()
            except Exception as E:
                return render_template('error.html', error_code=500, error_message="Při vytváření uživatele, při nové rezervaci, došlo k chybě!")

            id_uzivatel = Uzivatel.query.filter_by(email=email_uzivatel).first().id

        id_pokoj = int(request.form['id_pokoj'])
        id_hotel = int(request.form['id_hotel'])
        datum_zacatek = request.form['datum_zacatek']
        datum_konec = request.form['datum_konec']
        zaplaceno = True if request.form.get('zaplaceno') else False
        check_in = False
        finalni_cena = int(request.form['finalni_cena'])
        pocet_hostu = int(request.form['pocet_hostu'])

        rezervace = Rezervace(id_uzivatel=id_uzivatel, email_uzivatel=email_uzivatel, id_hotel=id_hotel,
                              id_pokoj=id_pokoj, datum_zacatek=datum_zacatek, datum_konec=datum_konec,
                              zaplaceno=zaplaceno, check_in=check_in, finalni_cena=finalni_cena, pocet_hostu=pocet_hostu)                              
        try:
            db.session.add(rezervace)
            db.session.commit()
        except Exception as E:
            return render_template('error.html', error_code=500, error_message="Při vytváření rezervace došlo k chybě!")
        
        if current_user.is_anonymous or current_user.role == "Zákazník":
            return redirect(url_for("everyone.offering"))
        
        return redirect(url_for("recepcni.reservations_management"))

    try:
        if request.form['override_url'] == "true":
            return redirect(url_for("index"))
    finally:
        return redirect(request.url)


# @create.route('/create_obrazek', methods=['POST'])
def create_obrazek(filename):
    obrazek = Obrazek(path_to_image=filename)
    try:
        db.session.add(obrazek)
        db.session.commit()
    except:
        return "Při registraci došlo k chybě!"

    return redirect(request.url)


@create.route('/create_vlastnik/<int:vlastnik_id>/<int:hotel_id>', methods=['POST'])
def create_vlastnik(vlastnik_id, hotel_id):
    if not current_user.is_anonymous and (current_user.role == "Admin" or current_user.role == "Vlastník"):
        vlastnik = Vlastnik(vlastnik_id=vlastnik_id, hotel_id=hotel_id)
        try:
            db.session.add(vlastnik)
            db.session.commit()
        except:
            return render_template('error.html', error_code=500, error_message="Při vytváření vlastníka došlo k chybě!")
    else:
        return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")

