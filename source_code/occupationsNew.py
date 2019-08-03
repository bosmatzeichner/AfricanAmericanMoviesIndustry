from imdb import IMDb
import json
import numpy as np
from SPARQLWrapper import SPARQLWrapper, JSON
import wikipedia
import requests
import nltk
from bs4 import BeautifulSoup

def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


careers_and_occupations = []
charactersPerJob = {}
def create_occupations_array():
    endpoint_url = "https://query.wikidata.org/sparql"

    query = """SELECT DISTINCT ?occLabel WHERE {
      ?occ wdt:P31 wd:Q28640.
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    
    """
    results = get_results(endpoint_url, query)

    for result in results["results"]["bindings"]:
        careers_and_occupations.append(result["occLabel"]["value"])
    careers_and_occupations.extend(["FBI Agent", "Agent","squad leader", ""])
    careers_and_occupations.sort()
    careers_and_occupations.sort(reverse=True, key=len)
    # charactersPerJobArr = {careers_and_occupations[i]:{'job':careers_and_occupations[i],'allActors': 0, 'actresses': 0, 'actors': 0} for i in range(len(careers_and_occupations))}
    # for job in charactersPerJobArr:
    #     print(job)

# ia = IMDb()

# -------------------------------- getting plot and find sentences containing a certain name------
def get_sentences_in_plot_contain_character(character_name, plot):
    arr = []

    stop_words = [character_name]
    # if ("'s " not in character_name) and ():
    #     stop_words = stop_words + character_name.split(' ')
    # print("characters optional names: ",stop_words)
    if plot:
        arr = [sent.lower().split(' ') for sent in plot.split('.') if any(word in sent for word in stop_words)]
        # print ("sentences array: ", arr)
        # arr = arr.split(' ')
    return arr
#  -------------------------------------- get character occupation in plot

def is_a_in_x(A, X):
    # print("len(x) = ", len(X))
    # print("len(A) = ", len(A))
    for i in range(len(X) - len(A) + 1):
        if A == X[i:i+len(A)]:
            return True
    return False


def get_character_occupation(sentence):
    # print("len(sentence): ", len(sentence))

    for job in careers_and_occupations:
        tmp = job
        tmp = tmp.split(' ')
        # print ("tmp is: ",tmp)
        if is_a_in_x(tmp, sentence):
        # if sentence[0].__contains__(job):
            return job


def get_occupation_by_plot(name , plot):
    char_sentences = get_sentences_in_plot_contain_character(name, plot)
    if char_sentences:
        # print("sentence 1 is:", char_sentences[0])
        return get_character_occupation(char_sentences[0])


def check_for_occupation(actor, plot):
    occupation = ''
    occupation = get_occupation_by_plot(actor["role"], plot)
    if occupation:
        print("\t\toccupation is from plot: " + occupation)
        return occupation
    for job in careers_and_occupations:
        tmp = job.lower()
        tmp = tmp.split(' ')
        if is_a_in_x(tmp, actor["role"].lower().split(' ')):
            occupation = job
            break
    if occupation:
        print("\t\toccupation is from role: " + occupation)
    return occupation


def get_plot(film_name):
    possibles = ['Plot', 'Synopsis', 'Plot synopsis', 'Plot summary',
                 'Story', 'Plotline', 'The Beginning', 'Summary',
                 'Content', 'Premise']
    plot = np.NaN
    possibles_edit = [i + 'Edit' for i in possibles]
    all_possibles = possibles + possibles_edit
    try:
        wik = wikipedia.WikipediaPage(film_name)
    except:
        wik = np.NaN
    try:
        for j in all_possibles:
            if wik.section(j) != None:
                plot = wik.section(j).replace('\n', '').replace("\'", "")
    except:
        plot = np.NaN

    return plot


def get_movie_actors_and_occupations(film_name, movie, black_actors):
    actors_with_occ = []
    print("for Movie: " + film_name)
    # actors = get_cast(movie['African American Actors'])
    plot = get_plot(film_name)
    if plot is np.NAN:
        plot = movie["overview"]
    # print('plot: ', plot)
    for actor in black_actors:
        # print("actor: {0}, played as: {1}".format(actor['name'], actor['role']))
        if(actor['role']):
            occupation = check_for_occupation(actor, plot)
            if occupation:
                print({'actor name': actor["name"], 'character name': actor["role"], 'occupation': occupation})
                actors_with_occ.extend([{'actor name': actor["name"], 'character name': actor["role"], 'occupation': occupation}])
                actor['occupation'] = occupation
                if (occupation in charactersPerJob):
                    charactersPerJob[occupation]['numOfCharacters'] += 1
                    charactersPerJob[occupation]['characters'].extend([{'movie name':film_name,'actor name': actor["name"], 'character name': actor["role"]}])
                else:
                    d = {occupation: {'numOfCharacters': 1,'characters': [{'movie name':film_name,'actor name': actor["name"], 'character name': actor["role"]}] }}
                    charactersPerJob.update(d)
    if actors_with_occ:
        print (actors_with_occ)
    return actors_with_occ


create_occupations_array()
print(careers_and_occupations)
yearsArray = ["19391969", "19691989","19892001", "20012007","20072011", "20112014","20142017", "20172019"]
moviesArrays={}


def read_jsons_to_arrays():
    for years in yearsArray:
        path = './MoviesDataWithBlackActors/moviesWith' + years + 'BlackActors.json'
        with open(path) as json_file:
            moviesArrays[years] = json.load(json_file)

    movies_res = []
    for years in yearsArray:
        path = './MoviesDataWithBlackActors/moviesWith'+years+'BlackActors.json'
        with open(path) as json_file:
            movies_res.extend(json.load(json_file))
    # print ("num of movies is: ",len(movies))
    return movies_res


movies = read_jsons_to_arrays()
i = 0

for years in moviesArrays:
    occupationsByMovieToJson = {}
    occupationsByJobToJson = []
    for movie in moviesArrays[years]:
        i += 1
        print("i is: ", i)
        film_name = movie['title']
        # actors = movie["Actors"]
        black_actors = movie['BlackActors']
        actors_with_occ = get_movie_actors_and_occupations(film_name,movie,black_actors)
        if actors_with_occ:
            occupationsByMovieToJson.update({film_name: {'actorsWithOcc': actors_with_occ}})
    occupationsByJobToJson = charactersPerJob
    open("./occupationsByJob"+years+".json", "w").write(json.dumps(occupationsByJobToJson, indent=4))
    open("./occupationsByMovie"+years+".json", "w").write(json.dumps(occupationsByMovieToJson, indent=4))

    open("./occupationsByJob.json", "a").write(json.dumps(occupationsByJobToJson, indent=4))
    open("./occupationsByMovie.json", "a").write(json.dumps(occupationsByMovieToJson, indent=4))





# get_movie_actors_and_occupations(film_name,movie,black_actors)
# if film_name != "The Polka King":
# if film_name != "Fist Fight":
# if film_name != "Jamesy Boy": #star/t
# actor: Tituss Burgess, played as: John The Physical Therapist ,for Movie: Catfight
#     continue
# if film_name != "The Shawshank Redemption": #star/t
#     continue
# The Shawshank Redemption 1994
