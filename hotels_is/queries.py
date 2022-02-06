from hotels_is.models import *
from flask import request


def get_hotels_from_database():
    hotels = Hotel.query.all()

    for hotel in hotels:
        hotel.vlastnici = []
        vlastnici = Vlastnik.query.filter_by(hotel_id=hotel.id)

        for vlastnik in vlastnici:
            uzivatel = Uzivatel.query.get(vlastnik.vlastnik_id)
            hotel.vlastnici.append(uzivatel)

    return hotels


def get_users_from_database():
    Uzivatele = Uzivatel.query.all()

    for uzivatel in Uzivatele:
        uzivatel.recepcni = Recepcni.query.filter_by(recepcni_id=uzivatel.id).first()
        uzivatel.vlastnik = Vlastnik.query.filter_by(vlastnik_id=uzivatel.id).first()

    return Uzivatele


# returns number of guests, all hotels (for select elements) and relevant rooms filtered by given filters 
def get_rooms_for_offer():
    if not request.method == "POST":
        filter = Filter(pocet_osob=1)
        rooms = Pokoj.query.limit(20).all()
        hotels = Hotel.query.all()
        return filter, hotels, rooms
    else:
        hotel_id = request.form['hotel_id']
        od = request.form['from']
        do = request.form['to']
        typ = request.form['room_type']
        seradit_podle = request.form['order_by']
        pocet_osob = request.form['num_of_guests']

        # args for query filter
        args = [Pokoj.pocet_luzek >= pocet_osob]
        if hotel_id != "":
            args.append(Pokoj.hotel_id == hotel_id)
        if typ != "":
            args.append(Pokoj.typ == typ)

        filter = Filter(pocet_osob=pocet_osob, hotel_id=hotel_id, od=od, do=do, typ=typ, seradit_podle=seradit_podle)
        rooms = Pokoj.query.filter(*args).all()

        if seradit_podle == "Nejvyšší cena":
            rooms = sorted(rooms, key=lambda x: x.cena_za_noc, reverse=True)
        elif seradit_podle == "Nejnižší cena":
            rooms = sorted(rooms, key=lambda x: x.cena_za_noc, reverse=False)
        else:
            pass

        if od != "" and do != "":
            tmp = []
            for room in rooms:
                reservation_start = Rezervace.query.filter(Rezervace.id_pokoj == room.id,
                                                           Rezervace.datum_zacatek.between(od, do)).first()
                reservation_end = Rezervace.query.filter(Rezervace.id_pokoj == room.id,
                                                         Rezervace.datum_konec.between(od, do)).first()
                if not (reservation_start or reservation_end):
                    tmp.append(room)
            rooms = tmp

        hotels = Hotel.query.all()
        return filter, hotels, rooms


class Filter:
    def __init__(self, pocet_osob, hotel_id=None, od=None, do=None, typ=None, seradit_podle=None):
        self.pocet_osob = int(pocet_osob) if pocet_osob is not None else pocet_osob
        self.hotel_id = int(hotel_id) if hotel_id is not None and hotel_id != "" else hotel_id
        self.od = od
        self.do = do
        self.typ = typ
        self.seradit_podle = seradit_podle
