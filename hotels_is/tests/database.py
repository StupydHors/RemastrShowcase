import datetime

from hotels_is import db
from hotels_is.models import *
from hotels_is.utils.passwords import hash_password


def fill_db_with_reference_data():
    db.drop_all()
    db.create_all()

    hotel1 = Hotel(name="Hotýlek Slovan", address="Mordor 42", rating=2)
    hotel2 = Hotel(name="Hotýlek Azure", address="Zotavovská 69", rating=4)
    hotel3 = Hotel(name="Hotýlek Moon", address="Cejl 43/88", rating=1)

    user1 = Uzivatel(email="zakaznik@hotylek.cz", password=hash_password("zakaznik"), role="Zákazník", name="Franta Trávníček", phone_number="+420756892365")
    user2 = Uzivatel(email="zakaznik2@hotylek.cz", password=hash_password("zakaznik"), role="Zákazník", name="Iveta Vopršálková", phone_number="+420559648125")
    user3 = Uzivatel(email="zakaznik3@hotylek.cz", password=hash_password("zakaznik"), role="Zákazník", name="Josef Strnadel", phone_number="+420789654321")
    user4 = Uzivatel(email="vlastnik@hotylek.cz", password=hash_password("vlastnik"), role="Vlastník", name="Lenka Smetana", phone_number="+420856984557")
    user5 = Uzivatel(email="recepcni@hotylek.cz", password=hash_password("recepcni"), role="Recepční", name="Zuzana Kamenná", phone_number="+420725648905")
    user6 = Uzivatel(email="recepcni2@hotylek.cz", password=hash_password("recepcni"), role="Recepční", name="Jan Novák", phone_number="+420608547965")
    user7 = Uzivatel(email="root", password=hash_password("root"), role="Admin", name="Alex Vítámvás", phone_number="+420568943218")

    db.session.add_all([user1, user2, user3, user4, user5, user6, user7, hotel1, hotel2, hotel3])
    db.session.commit()

    recepcni1 = Recepcni(hotel_id=hotel1.id, recepcni_id=user5.id)
    recepcni2 = Recepcni(hotel_id=hotel3.id, recepcni_id=user6.id)
    vlastnik1 = Vlastnik(vlastnik_id=user4.id, hotel_id=hotel1.id)
    db.session.add_all([recepcni1, recepcni2, vlastnik1])
    db.session.commit()

    obrazek1 = Obrazek(path_to_image="pokoj_1.jpg")
    obrazek2 = Obrazek(path_to_image="pokoj_2.jpg")
    obrazek3 = Obrazek(path_to_image="pokoj_3.jpg")
    obrazek4 = Obrazek(path_to_image="pokoj_4.jpg")

    db.session.add_all([obrazek1, obrazek2, obrazek3, obrazek4])
    db.session.commit()

    pokoj1 = Pokoj(hotel_id=hotel1.id, cislo=69, cena_za_noc=450, pocet_luzek=3, typ="standard", velikost="3+1",
                   klimatizace=True, balkon=True, pristylka=True, fotka_id=obrazek1.id)
    pokoj2 = Pokoj(hotel_id=hotel2.id, cislo=42, cena_za_noc=750, pocet_luzek=2, typ="business", velikost="2+1",
                   klimatizace=True, balkon=False, pristylka=True, fotka_id=obrazek2.id)
    pokoj3 = Pokoj(hotel_id=hotel3.id, cislo=632, cena_za_noc=650, pocet_luzek=5, typ="standard", velikost="1+1",
                   klimatizace=True, balkon=False, pristylka=False, fotka_id=obrazek3.id)
    pokoj4 = Pokoj(hotel_id=hotel1.id, cislo=123, cena_za_noc=550, pocet_luzek=3, typ="president", velikost="1+1",
                   klimatizace=False, balkon=True, pristylka=False, fotka_id=obrazek4.id)

    db.session.add_all([pokoj1, pokoj2, pokoj3, pokoj4])
    db.session.commit()

    rezervace1 = Rezervace(id_uzivatel=user1.id, email_uzivatel=user1.email, id_hotel=hotel1.id, id_pokoj=pokoj2.id,
                           datum_zacatek=datetime.date.today(),
                           datum_konec=datetime.date.today() + datetime.timedelta(days=1), zaplaceno=True, check_in=False,
                           pocet_hostu=2, finalni_cena=1500, check_out=False, potvrzeno=True)
    rezervace2 = Rezervace(id_uzivatel=user2.id, email_uzivatel=user2.email, id_hotel=hotel3.id, id_pokoj=pokoj3.id,
                           datum_zacatek=datetime.date.today(),
                           datum_konec=datetime.date.today() + datetime.timedelta(days=3), zaplaceno=False, check_in=False,
                           pocet_hostu=1, finalni_cena=650, check_out=False, potvrzeno=True)

    db.session.add_all([rezervace1, rezervace2])
    db.session.commit()
