from flask import Markup
from flask_appbuilder.filemanager import ImageManager
from flask_appbuilder.models.mixins import ImageColumn
from flask_login import UserMixin

from hotels_is import db, login_manager


@login_manager.user_loader
def load_user(id):
    return Uzivatel.query.get(int(id))


# Tabulka uživatelů (všech)
class Uzivatel(db.Model, UserMixin):
    __tablename__ = 'uzivatele'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=True)
    name = db.Column(db.Unicode(512), nullable=False)
    phone_number = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Unicode(20), nullable=True)


# Tabulka rezevrací
class Rezervace(db.Model):
    __tablename__ = 'rezervace'
    id = db.Column(db.Integer, primary_key=True)
    id_uzivatel = db.Column(db.Integer, db.ForeignKey('uzivatele.id'), nullable=True)
    email_uzivatel = db.Column(db.String(128), unique=False, nullable=False)
    id_pokoj = db.Column(db.Integer, db.ForeignKey('pokoje.id'), nullable=False)
    id_hotel = db.Column(db.Integer, db.ForeignKey('hotely.id'), nullable=False)
    pocet_hostu = db.Column(db.Integer)
    datum_zacatek = db.Column(db.Date)
    datum_konec = db.Column(db.Date)
    zaplaceno = db.Column(db.Boolean)
    check_in = db.Column(db.Boolean)
    check_out = db.Column(db.Boolean)
    potvrzeno = db.Column(db.Boolean)
    finalni_cena = db.Column(db.Integer)


# Tabulka pokojů
class Pokoj(db.Model):
    __tablename__ = 'pokoje'
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotely.id'), nullable=False)
    cislo = db.Column(db.Integer)
    cena_za_noc = db.Column(db.Integer)
    pocet_luzek = db.Column(db.Integer)
    typ = db.Column(db.String(64))
    velikost = db.Column(db.String(64))
    klimatizace = db.Column(db.Boolean)
    balkon = db.Column(db.Boolean)
    pristylka = db.Column(db.Boolean)
    fotka_id = db.Column(db.Integer, db.ForeignKey('obrazek.id'), nullable=True)

    def get_pokoj_image(self):
        if self.fotka_id is None:
            return None
        else:
            return Obrazek.query.get(self.fotka_id).this_img_path()


# Tabulka hotelů
class Hotel(db.Model):
    __tablename__ = 'hotely'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(128), nullable=False)
    address = db.Column(db.Unicode(128), nullable=False)
    rating = db.Column(db.Integer)
    fotka_id = db.Column(db.Integer, db.ForeignKey('obrazek.id'), nullable=True)


# Tabulka recepčních (vztah uživatel-hotel)
class Recepcni(db.Model):
    __tablename__ = 'recepcni'
    recepcni_id = db.Column(db.Integer, db.ForeignKey('uzivatele.id'), primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotely.id'))
    recepcni = db.relationship("Uzivatel", foreign_keys=[recepcni_id])
    hotel = db.relationship("Hotel", foreign_keys=[hotel_id])


# Tabulka vlastníků (vztah vlastník-hotel)
class Vlastnik(db.Model):
    __tablename__ = 'vlastnici'
    vlastnik_id = db.Column(db.Integer, db.ForeignKey('uzivatele.id'), primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotely.id'), primary_key=True)


# Tabulka obrázků
class Obrazek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path_to_image = db.Column(ImageColumn(thumbnail_size=(100, 100, True), size=(500, 500, True)), nullable=False)

    hotel = db.relationship('Hotel', backref='fotka', lazy=False)
    pokoj = db.relationship('Pokoj', backref='fotka', lazy=False)

    def this_img(self):
        im = ImageManager()
        if self.path_to_image:
            return Markup(
                '<img src="' +
                im.get_url(self.path_to_image) +
                '" alt="Photo" class="img-rounded img-responsive">'
            )
        else:
            return Markup(
                '<img src="//:0" alt="Photo" class="img-responsive">'
            )

    def this_img_path(self):
        im = ImageManager()
        if self.path_to_image:
            return im.get_url(self.path_to_image)
        else:
            return 'src="//:0"'

    def get_image_name(self):
        return self.path_to_image

    def __repr__(self):
        return self.get_image_name()
