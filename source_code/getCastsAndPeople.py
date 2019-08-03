import http.client
import json
import time
import imdb

ia = imdb.IMDb()
with open('movieData20172019.json') as json_file:
    data = json.load(json_file)
flat_data = [item for sublist in data for item in sublist]

person = []
# person = [ 0 for _ in range(2800000)]
conn = http.client.HTTPSConnection("api.themoviedb.org")
people = []

# change it to get cast from tmdb or change to actors ids of tmdb and not imdb !
def get_cast(movie):
    # print (movie)
    movieName =movie["title"]
    result = ia.search_movie(movieName)
    if result:
        movieID = ia.get_movie(result[0].movieID)
    if (movieID):
        cast = movieID.get('cast')
        if cast:
            print (cast)
    return cast

    return

def initiate_people_list():
    for movie in flat_data:
        cast = get_cast(movie)
        if (cast == None):
            continue
        for actor in cast:
            personId = actor.personID
            print("person id: "+personId+", name: "+actor["name"])
            # index = int(personId)
            # print("index: ", index)
            person[index] = 1
            # person.append(personId)
    return

def get_people():
    for i in len(person): #49618
        if(person[i]==0):
            continue
        payload = "{}"
        req = "https://api.themoviedb.org/3/person/%d?api_key=5c1eeb331ccdc877d96b634737ed2560&language=en-US" %(i)
        conn.request("GET",req , payload)
        res = conn.getresponse()
        while res.status_code == 429:
            res = conn.getresponse()
        data = res.read()
        datastr = data.decode("utf-8")
        if datastr == '{"status_code":34,"status_message":"The resource you requested could not be found.","success":false}':
            continue
        people.append(datastr)

    people_array = []
    for person in people:
        parsed = json.loads(person)
        people_array.append(parsed)


    dataFileActors = open("./actorsData20000.json", "a")
    dataFileProducers = open("./producersData20000.json", "a")
    dataFileDirectors = open("./DirectorsData20000.json", "a")
    actors_array = []
    producers_array = []
    directors_array = []

    for person in people_array:
        dep = person["known_for_department"]
        if dep == "Acting":
            actors_array.append(person)

    dataFileActors.write(json.dumps(actors_array, indent=4))

    for person in people_array:
            dep = person["known_for_department"]
            if dep == "Production":
                producers_array.append(person)

    dataFileProducers.write(json.dumps(producers_array, indent=4))

    for person in people_array:
            dep = person["known_for_department"]
            if dep == "Directing":
                directors_array.append(person)

    dataFileDirectors.write(json.dumps(directors_array, indent=4))

initiate_people_list()
get_people()