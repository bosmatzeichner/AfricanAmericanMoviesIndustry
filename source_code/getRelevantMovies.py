import json
import requests
from bs4 import BeautifulSoup
import imdb


def getActor(actor, movie):
    actorName = actor['name']
    actorName = actorName.replace(" ", "_")
    getUrl = 'https://en.wikipedia.org/wiki/' + actorName
    url = getUrl
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    QNumber = soup.find('li', {'id': 't-wikibase'})
    if QNumber == None:
        return -1
    QNumber = QNumber.a['href'].rsplit('/')[-1]
    url = 'https://query.wikidata.org/sparql'
    query = """
                SELECT (SAMPLE(?actor) AS ?actor)
                WHERE {
                     VALUES ?actor { wd:""" + QNumber + """}
                     {?actor wdt:P106 wd:Q10800557. ?actor wdt:P172 wd:Q49085.}
                     UNION
                     {?actor wdt:P106 wd:Q33999. ?actor wdt:P172 wd:Q49085.}

                 SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                 }
                  """
    r = requests.get(url, params={'format': 'json', 'query': query})
    while r.status_code == 429:
        r = requests.get(url, params={'format': 'json', 'query': query})
    rjson = r.json()
    bindings = rjson['results']['bindings']
    if bindings == [{}]:
        return -1
    africanAmreicanArr = movie["African American Actors"]
    role = actor.currentRole
    dict = {'name': actor['name'], 'role': str(role), 'QNumber': QNumber}
    africanAmreicanArr.append(dict)



with open('movieData20172019.json') as json_file:
    data = json.load(json_file)

flat_data = [item for sublist in data for item in sublist]

movieNames_array = []
relevantMoviesArr = []
counter = 1

relevantMoviesNew = open("./relevantMovies.json", "a")

for movie in flat_data:
    movie["African American Actors"] = []
    print("movie: ", movie["title"])
    counter = counter + 1
    if(counter > 20):
        break
    movieName =movie["title"]
    movieNames_array.append(movieName)
    movieName = movieName.replace(" ", "_")
    ia = imdb.IMDb()
    result = ia.search_movie(movieName)
    blackActorsCounter = 0
    if result:
        movieID = ia.get_movie(result[0].movieID)
        print("movieId: ", movieID)
        if (movieID):
            cast = movieID.get('cast')
            if(cast == None):
                continue
            for actor in cast:
                if(getActor(actor,movie) == -1):
                    continue
            if movie["African American Actors"] != []:
                relevantMoviesArr.append(movie);

#flat_relevantMoviesArr = [item for sublist in relevantMoviesArr for item in sublist]
print("relevant movies Arr : " ,relevantMoviesArr)
relevantMoviesNew.write(json.dumps(relevantMoviesArr, indent=4))



