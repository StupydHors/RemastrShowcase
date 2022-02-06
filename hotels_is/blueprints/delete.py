from flask import Blueprint, abort, request, url_for, render_template, flash
import flask
from jinja2 import TemplateNotFound
from werkzeug.utils import redirect
from flask_login import current_user
from hotels_is.utils.passwords import verify_password

from hotels_is.models import *

delete = Blueprint('delete', __name__,
                   template_folder='templates')


# show update page
@delete.route('/<string:entity>', methods=['GET'])
def delete_entity(entity):
    if entity == "uzivatel":
        if not current_user.is_anonymous and current_user.role == "Admin":
            try:
                uzivatel = Uzivatel.query.get_or_404(request.args.get('id'))
                db.session.delete(uzivatel)
                db.session.commit()
            except Exception:
                return render_template('error.html', error_code=500, error_message="Při snaze odstranit uživatele došlo k chybě!")

            return redirect(url_for("admin.users_management"))

        else:
            return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")

    elif entity == "hotel":
        if not current_user.is_anonymous and (current_user.role == "Admin" or current_user.role == "Vlastník"):
            try:
                vlastnik = Vlastnik.query.filter_by(hotel_id=request.args.get('id')).delete()
                db.session.commit()

                hotel = Hotel.query.get_or_404(request.args.get('id'))
                db.session.delete(hotel)
                db.session.commit()
            except Exception as e:
                print(e)
                return render_template('error.html', error_code=500, error_message="Při snaze odstranit hotel došlo k chybě!")

            return redirect(url_for("vlastnik.hotels_management"))

        else:
            return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")


    elif entity == "pokoj":
        if not current_user.is_anonymous and (current_user.role == "Admin" or current_user.role == "Vlastník"):
            try:
                pokoj = Pokoj.query.get_or_404(request.args.get('id'))
                db.session.delete(pokoj)
                db.session.commit()
            except Exception:
                return render_template('error.html', error_code=500, error_message="Při snaze odstranit pokoj došlo k chybě!")

            return redirect(url_for("vlastnik.rooms_management"))
        
        else:
            return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")

    elif entity == "rezervace":
        if not current_user.is_anonymous:
            try:
                rez = Rezervace.query.get_or_404(request.args.get('id'))
                db.session.delete(rez)
                db.session.commit()
            except Exception:
                return render_template('error.html', error_code=500, error_message="Při snaze odstranit rezervaci došlo k chybě!")

            if current_user.role == "Zákazník":
                return redirect(url_for("zakaznik.my_reservations"))
            return redirect(url_for("recepcni.reservations_management"))
        
        else:
            return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")

    elif entity == "obrazek":
        if not current_user.is_anonymous and (current_user.role == "Admin" or current_user.role == "Vlastník"):
            try:
                obrazek = Obrazek.query.get_or_404(request.args.get('id'))
                db.session.delete(obrazek)
                db.session.commit()
            except Exception:
                return render_template('error.html', error_code=500, error_message="Při snaze odstranit obrázek došlo k chybě!")

            return redirect(url_for("obrazek.obrazek_base"))
        
        else:
            return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")

    return redirect(url_for("admin.dashboard"))


@delete.route('/delete_vlastnik/<int:vlastnik_id>/<int:hotel_id>', methods=['POST'])
def delete_vlastnik(vlastnik_id, hotel_id):
    if not current_user.is_anonymous and current_user.role == "Admin":
        try:
            vlastnik = Vlastnik.query.filter_by(vlastnik_id=vlastnik_id, hotel_id=hotel_id).first()
            db.session.delete(vlastnik)
            db.session.commit()
        except Exception:
            return render_template('error.html', error_code=500, error_message="Při snaze odstranit vlastníka došlo k chybě!")

    else:
        return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")

@delete.route('/profile', methods=['POST'])
def delete_profile():
    if not current_user.is_anonymous:
        if verify_password(current_user.password, request.form['password']): 
            try:
                uzivatel = Uzivatel.query.get(current_user.id)
                db.session.delete(uzivatel)
                db.session.commit()
                return redirect(url_for('logout'))
            except Exception:
                return render_template('error.html', error_code=500, error_message="Při snaze odstranit profil došlo k chybě!")
        else:
            flash("Hesla se neshodují.")
            flash("Požadavek se nezdařil.")

        return redirect(request.referrer)

    else:
        return render_template('error.html', error_code=401, error_message="Neoprávněná modifikace databáze!")
