import json
import time
from geopy.geocoders import Nominatim
# with open('./africanAmericanActorsData.json') as json_file:
#     actors = json.load(json_file)
#
# with open('./africanAmericanDirectorsData.json') as json_file:
#     directors = json.load(json_file)
#
# with open('./africanAmericanProducersData.json') as json_file:
#     producers = json.load(json_file)
#
#
# # nameOfGroup = actors/directors/producers
# def get_birth_places(people, nameOfGroup):
#     birth_places = {}
#     for p in people:
#         birth_place = p["place_of_birth"]
#         if birth_place:
#             if birth_place in birth_places:
#                 birth_places[birth_place]["numOf"+nameOfGroup] += 1
#                 birth_places[birth_place][nameOfGroup].extend([p['name']])
#             else:
#                 d = {birth_place: {"numOf"+nameOfGroup: 1, nameOfGroup: [p["name"]]}}
#                 birth_places.update(d)
#     return birth_places
#
#
# actorsBirthPlaces = get_birth_places(actors, "Actors")
# open("./actorsBirthPlaces.json", "w").write(json.dumps(actorsBirthPlaces, indent=4))
#
# directorsBirthPlaces = get_birth_places(directors, "Directors")
# open("./directorsBirthPlaces.json", "w").write(json.dumps(directorsBirthPlaces, indent=4))
#
# producersBirthPlaces = get_birth_places(producers, "Producers")
# open("./producersBirthPlaces.json", "w").write(json.dumps(producersBirthPlaces, indent=4))



# def change_to_legal_json(people):
#     with open('./'+people+'BirthPlaces.json') as json_file:
#         birthPlaces = json.load(json_file)
#     a=[]
#     for place in birthPlaces:
#         birthPlaces[place].update({'place': place})
#         a.extend([birthPlaces[place]])
#     open("./"+people+"BirthPlacesNew.json", "w").write(json.dumps(a, indent=4))
#
#
# change_to_legal_json("actors")
# change_to_legal_json("directors")
# change_to_legal_json("producers")

# counter = 0
# with open('./producersBirthPlacesNew.json') as json_file:
#  birthPlaces = json.load(json_file)
#  for item in birthPlaces:
#     time.sleep(1)
#     counter+=1
#     print(counter)
#     print(item)
#     place = item['place']
#     geolocator = Nominatim(user_agent="my-application", timeout=None)
#     location = geolocator.geocode(place)
#     item['latitude'] = location.latitude
#     item['longitude'] = location.longitude
# open("./producersBirthPlacesWithCoordinates.json", "a").write(json.dumps(birthPlaces, indent=4))

# geolocator = Nominatim(user_agent="my-application", timeout=None)
# location = geolocator.geocode("Trenton, New Jersey, USA")
# print(location.latitude, location.longitude)

with open('./producersBirthPlacesWithCoordinates.json') as json_file:
 birthPlaces = json.load(json_file)
birthPlacesNew = []
for i in range(0, len(birthPlaces)):
    lat1 = birthPlaces[i]['latitude']
    long1 = birthPlaces[i]['longitude']
    numOfProducers = birthPlaces[i]['numOfProducers']
    Producers = birthPlaces[i]['Producers']
    place = birthPlaces[i]['place']
    for j in range(i+1, len(birthPlaces)):
        lat2 = birthPlaces[j]['latitude']
        long2 = birthPlaces[j]['longitude']
        if lat1==lat2 and long1==long2:
            numOfProducers = numOfProducers + birthPlaces[j]['numOfProducers']
            Producers.extend(birthPlaces[j]['Producers'])
            birthPlaces[j]['latitude'] = j
            birthPlaces[j]['longitude'] = j
    toAdd = [{'numOfProducers': numOfProducers, 'Producers': Producers, 'place': place, 'latitude': lat1, 'longitude': long1}]
    birthPlacesNew.extend(toAdd)
birthPlacesNewFixed = []
for item in birthPlacesNew:
    if type(item['longitude']) is float:
        birthPlacesNewFixed.append(item)
open("./producersBirthPlacesWithCoordinatesFixed.json", "a").write(json.dumps(birthPlacesNewFixed, indent=4))

