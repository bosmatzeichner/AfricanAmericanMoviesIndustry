import http.client
import json
import time

conn = http.client.HTTPSConnection("api.themoviedb.org")
actorsId = [0] * 2365455
directorsId = [0] * 2365455
producersId = [0] * 2365455




conn = http.client.HTTPSConnection("api.themoviedb.org")
i = 0
counter = 0
yearsArray = ["movieData20072011.json"]

for year in yearsArray:
    with open(year) as json_file:
        movies = json.load(json_file)
    flat_movies = [item for sublist in movies for item in sublist]
    for movie in flat_movies:
        # counter +=1
        # if(counter > 50):
        #     break
        i = i + 1
        print("i is: ", i)
        if i % 40 == 0:
            time.sleep(10)
        movieId = movie['id']
        print("movie id is: " , movieId)
        payload = "{}"
        req = "/3/movie/%d/credits?api_key=5c1eeb331ccdc877d96b634737ed2560" %(movieId)
        conn.request("GET",req, payload)
        res = conn.getresponse()
        data = res.read()
        datastr = data.decode("utf-8")
        if datastr == '{"status_code":34,"status_message":"The resource you requested could not be found."}':
            continue
        parsed = json.loads(datastr)
        print(parsed)
        cast = parsed['cast']
        for actor in cast:
            actorId = actor['id']
            actorsId[actorId] = 1
        crew = parsed['crew']
        for crewMem in crew:
            crewMemId = crewMem['id']
            department = crewMem['department']
            if(department == "Directing"):
                directorsId[crewMemId] = 1
            elif(department == "Production"):
                producersId[crewMemId] = 1

dataFile = open("./PeopleArrays20072011.json", "a")


dataFile.write(json.dumps(dict))