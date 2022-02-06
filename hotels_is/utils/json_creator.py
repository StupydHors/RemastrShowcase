from hotels_is.models import *

def create_hotels_json():
    hotels = Hotel.query.all()
    hotels_json = "["
    for hotel in hotels:
        hotels_json += "{"
        hotels_json += "\"id\":{0}, \"name\":\"{1}\"".format(hotel.id, hotel.name)
        hotels_json += "},"
    hotels_json = hotels_json[0:-1]
    hotels_json += "]"
    return hotels_json