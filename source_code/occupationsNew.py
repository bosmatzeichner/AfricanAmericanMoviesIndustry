import json
import numpy as np
from SPARQLWrapper import SPARQLWrapper, JSON
import wikipedia


yearsArray = ["19391969", "19691989","19892001", "20012007","20072011", "20112014","20142017", "20172019"]
careers_and_occupations = []


def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


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


def get_sentences_in_plot_contain_character(character_name, plot):
    arr = []
    stop_words = [character_name]
    if plot:
        # added replace(',','') on 4.8 while realized that a comma can be right after occupation
        arr = [sent.lower().replace(',','').split(' ') for sent in plot.split('.') if any(word in sent for word in stop_words)]
    return arr


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


def get_movie_actors_and_occupations(charactersPerJob, film_name, movie, black_actors):
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
                if occupation in charactersPerJob.keys():
                    charactersPerJob[occupation]['numOfCharacters'] += 1
                    charactersPerJob[occupation]['characters'].extend([{'movie name':film_name,'actor name': actor["name"], 'character name': actor["role"]}])
                else:
                    print("this is occupation:", occupation)
                    d = {occupation: {'numOfCharacters': 1,'characters': [{'movie name':film_name,'actor name': actor["name"], 'character name': actor["role"]}] }}
                    charactersPerJob.update(d)
    if actors_with_occ:
        print (actors_with_occ)
    return actors_with_occ


def read_jsons_to_arrays():
    moviesArrays = {}
    for years in yearsArray:
        path = './MoviesDataWithBlackActors/moviesWith' + years + 'BlackActors.json'
        with open(path) as json_file:
            moviesArrays[years] = json.load(json_file)
    return moviesArrays


def create_occupations_by_job_and_by_movies_jsons():
    create_occupations_array()
    print(careers_and_occupations)
    movies_arrays = read_jsons_to_arrays()
    for years in movies_arrays:
        i = 0
        charactersPerJob = {}
        occupationsByMovieToJson = {}
        for movie in movies_arrays[years]:
            i += 1
            print("i is: ", i)
            film_name = movie['title']
            black_actors = movie['BlackActors']
            actors_with_occ = get_movie_actors_and_occupations(charactersPerJob, film_name, movie, black_actors)
            if actors_with_occ:
                occupationsByMovieToJson.update({film_name: {'actorsWithOcc': actors_with_occ}})
        open("./occupations_dicts/occupationsByJob" + years + ".json", "w").write(json.dumps(charactersPerJob, indent=4))
        open("./occupations_dicts/occupationsByMovie" + years + ".json", "w").write(json.dumps(occupationsByMovieToJson, indent=4))


def create_same_dict_with_title(d, by_what, to_update):
    d['title'] = by_what
    d.update(to_update)
    return d


def add_or_update_merged_jobs_dict(merged_jobs, job, file):
    if job in merged_jobs.keys():
        merged_jobs[job]['numOfCharacters'] += file[job]['numOfCharacters']
        merged_jobs[job]['characters'].extend(file[job]['characters'])
    else:
        # create_same_dict_with_title(merged_jobs[job], job, file[job])
        merged_jobs[job]={}
        merged_jobs[job]['title'] = job
        merged_jobs[job].update(file[job])

def refile(by_what, f, new_file):
    path = "./occupations_new/occupationsBy" + by_what + f + "New.json"
    open(path, "w").write(json.dumps(new_file, indent=4))


def save_merged(by_what,occupations_by):
    path = "./occupations_new/occupationsBy"+by_what+"Merged.json"
    open(path, "w").write(json.dumps(occupations_by, indent=4))


def read_files(by_what):
    files = {}
    for years in yearsArray:
        path = "./occupations_dicts/occupationsBy" + by_what + years + ".json"
        with open(path) as json_file:
            files[years] = json.load(json_file)
    return files


def create_legal_jobs_jsons():
    job_files = read_files("Job")
    mergedjobs = {}
    for f in job_files:
        new_file = []
        for job in job_files[f]:
            add_or_update_merged_jobs_dict(mergedjobs, job, job_files[f])
            new_file.extend([create_same_dict_with_title({},job, job_files[f][job])])
            refile("Job", f,new_file)
    occupations_by_job = []
    # print (mergedjobs)
    for job in mergedjobs.values():
        occupations_by_job.extend([job])
    save_merged("Jobs",occupations_by_job)


def create_legal_movies_jsons():
    movies_files = read_files("Movie")
    occupations_by_movie = []
    for f in movies_files:
        new_file = []
        file = movies_files[f]
        for movie in file:
            dict_movie = create_same_dict_with_title({},movie, file[movie])
            occupations_by_movie.extend([dict_movie])
            new_file.extend([dict_movie])
        refile("Movie", f,new_file)

    save_merged("Movies",occupations_by_movie)


create_occupations_by_job_and_by_movies_jsons()
create_legal_jobs_jsons()
create_legal_movies_jsons()
