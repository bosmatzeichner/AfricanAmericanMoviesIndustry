
import http.client
import json
import time



def open_json_file(name):
    with open(name) as json_file:
        data = json.load(json_file)
    return data

def open_flat_json_file(name):
    data = open_json_file(name)
    flat_data = [item for sublist in data for item in sublist]
    return flat_data


def addToBlackList(memId,array,africanAmericanPeople,dict):
    for blackProducer in africanAmericanPeople:
        if memId == blackProducer['id']:
            array.append(dict)
            break


def add_cast_and_crew(parsed,movie):
        cast = parsed['cast']
        for actor in cast:
            dict = {'actorId':actor['id'],'name': actor['name'], 'role': actor['character']}
            movie["Actors"].append(dict)
            addToBlackList(actor['id'],movie["BlackActors"], africanAmericanActors, dict)
        crew = parsed['crew']
        for crewMem in crew:
            crewMemId = crewMem['id']
            department = crewMem['department']
            if(department == "Directing"):
                dict = {'directorId': crewMemId, 'name': crewMem['name']}
                movie["Directors"].append(dict)
                addToBlackList(crewMemId,movie["BlackDirectors"],africanAmericanDirectors,dict)
            elif(department == "Production"):
                dict = {'directorId': crewMemId, 'name': crewMem['name']}
                movie["Producers"].append(dict)
                addToBlackList(crewMemId,movie["BlackProducers"],africanAmericanProducers,dict)


def add_new_fields(movie):
    movie["Actors"] = []
    movie["Directors"] = []
    movie["Producers"] = []
    movie["BlackActors"] = []
    movie["BlackDirectors"] = []
    movie["BlackProducers"] = []


def get_datastr(conn,movieId):
    payload = "{}"
    req = "/3/movie/%d/credits?api_key=5c1eeb331ccdc877d96b634737ed2560" % (movieId)
    conn.request("GET", req, payload)
    res = conn.getresponse()
    data = res.read()
    datastr = data.decode("utf-8")
    if datastr == '{"status_code":34,"status_message":"The resource you requested could not be found."}':
        return -1
    return datastr


def create_json_with_members(years):
    print("adding members to movies from years: "+years)
    name = 'movieData'+years+'.json'
    flat_data = open_flat_json_file(name)
    conn = http.client.HTTPSConnection("api.themoviedb.org")
    i = 0
    counter = 1
    moviesWithBlackActors = []
    moviesWithBlackDirectors = []
    moviesWithBlackProducers = []
    for movie in flat_data:
        add_new_fields(movie)
        counter +=1
        # if(counter > 50):
        #     break
        i = i + 1
        print("i is: ", i)
        if i % 40 == 0:
            time.sleep(10)
        movieId = movie['id']
        print("movie id is: " , movieId)
        datastr = get_datastr(conn,movieId)
        if datastr == -1:
            continue
        parsed = json.loads(datastr)
        add_cast_and_crew(parsed,movie)
        if(movie['BlackActors'] != []):
            moviesWithBlackActors.append(movie)
        if(movie['BlackDirectors'] != []):
            moviesWithBlackDirectors.append(movie)
        if(movie['BlackProducers']!= []):
            moviesWithBlackProducers.append(movie)

    open("./" +"movies"+years+"withMembers.json", "w").write(json.dumps(flat_data, indent=4))
    open("./" + "moviesWith" + years + "BlackActors.json", "w").write(json.dumps(moviesWithBlackActors, indent=4))
    open("./" + "moviesWith" + years + "BlackDirectors.json", "w").write(json.dumps(moviesWithBlackDirectors, indent=4))
    open("./" + "moviesWith" + years + "BlackProducers.json", "w").write(json.dumps(moviesWithBlackProducers, indent=4))


yearsArray = ["20172019"]
africanAmericanActors = open_json_file('africanAmericanActorsData.json')
africanAmericanDirectors = open_json_file('africanAmericanDirectorsData.json')
africanAmericanProducers = open_json_file('africanAmericanProducersData.json')

for years in yearsArray:
    create_json_with_members(years)
    time.sleep(3)