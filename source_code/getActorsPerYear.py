import json
import requests
from bs4 import BeautifulSoup
import imdb

def open_json_file(name):
    with open(name) as json_file:
        data = json.load(json_file)
    return data

def getYear(movie):
    date = movie['release_date']
    year = int(date.split('-')[0])
    return year

def getGender(actorId):
    name = "./AfricanAmericanActors/africanAmericanActorsData.json"
    data = open_json_file(name)
    for actor in data:
        if actorId == actor['id']:
            return actor['gender']

def getActors(movie):
    return movie["BlackActors"]

def countActorsPerYear(data):
    for movie in data:
        year = getYear(movie)
        actors = getActors(movie)
        numOfActors = len(actors)
        actorsPerYearArr[year - 1939]['year'] = year
        actorsPerYearArr[year - 1939]['allActors'] += numOfActors
        for actor in actors:
            gender = getGender(actor['actorId'])
            if gender == 1:
                actorsPerYearArr[year - 1939]['actresses'] += 1
            elif gender == 2:
                actorsPerYearArr[year - 1939]['actors'] += 1
            elif gender == 0:
                actorsPerYearArr[year - 1939]['noGender'] += 1


def countAllMoviesPerYear(data):
    for movie in data:
        year = int(getYear(movie))
        allMoviesPerYearArr[year - 1939]['year'] = year
        allMoviesPerYearArr[year - 1939]['movies'] += 1

yearsArray = ["19391969", "19691989", "19892001", "20012007", "20072011", "20112014", "20142017", "20172019"]
actorsPerYearArr = [{'year': None , 'allActors': 0, 'actresses': 0, 'actors': 0, 'noGender' : 0} for _ in range(81)]
#relevantMoviesPerYearArr = [{'year': None , 'movies': 0} for _ in range(81)]
allMoviesPerYearArr = [{'year': None , 'movies': 0} for _ in range(81)]

for year in yearsArray:
    name = "./MoviesDataWithoutMembers/movieData" + year +".json"
    data = open_json_file(name)
    flat_data = [item for sublist in data for item in sublist]
    countAllMoviesPerYear(flat_data)

for year in yearsArray:
   name = "./MoviesDataWithBlackActors/moviesWith" + year + "BlackActors.json"
   data = open_json_file(name)
   countActorsPerYear(data)




dataFileMoviesPerYear = open("./moviesPerYear.json", "a")
# parsed_array = []
# for year in allMoviesPerYearArr:
#     parsed = json.loads(year)
#     #parsed = parsed["results"]
#     parsed_array.append(parsed)
dataFileMoviesPerYear.write(json.dumps(allMoviesPerYearArr, indent=4))
dataFileActorsPerYear = open("./actorsPerYear.json", "a")
# parsed_array = []
# for year in actorsPerYearArr:
#     parsed = json.loads(year)
#     #parsed = parsed["results"]
#     parsed_array.append(parsed)
dataFileActorsPerYear.write(json.dumps(actorsPerYearArr, indent=4))
