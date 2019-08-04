import json
import requests
import imdb

def read_jsons_to_arrays():
    yearsArray = ["19391969", "19691989","19892001", "20012007","20072011", "20112014","20142017", "20172019"]
    movies_res = []
    for years in yearsArray:
        path = './MoviesDataWithBlackActors/moviesWith'+years+'BlackActors.json'
        with open(path) as json_file:
            movies_res.extend(json.load(json_file))
    # print ("num of movies is: ",len(movies))
    return movies_res


def add_num_of_movies(actor1,actors):
    africanAmericanActorsPath = "./AfricanAmerican"+actors+"./africanAmerican"+actors+"Data.json"
    with open(africanAmericanActorsPath) as json_file:
        blackActors = json.load(json_file)
    counter = 0
    for actor in blackActors:
        counter+=1
        print(counter)
        actor['numOfMovies'] = 0
    for actor in blackActors:
        if(actor['name'] == "Tim Moore"):
            continue
        for movie in movies:
            for record in movie["Black" + actors]:
                str = actor1+ "Id"
                if actor['id'] == record[str]:
                    actor['numOfMovies'] += 1
    sortedData = sorted(blackActors, reverse=True, key=lambda i: i['numOfMovies'])
    open("./black"+actors+"WithNumOfMovies.json", "w").write(json.dumps(sortedData, indent=4))
    mostPopular = sortedData[:10]
    dataFileMostPopular = open("./top10"+actors+".json", "w")
    dataFileMostPopular.write(json.dumps(mostPopular, indent=4))

    base_url = "http://image.tmdb.org/t/p/"
    size = "w185"
    for item in mostPopular:
        name = item['name']
        if(name == "James Lassiter"):
            continue
        path = item['profile_path']
        url = base_url + size + path
        r = requests.get(url)
        filetype = r.headers['content-type'].split('/')[-1]
        filename = 'poster_{0}.{1}'.format(name, filetype)
        with open(actors + "Pics/" + filename, 'wb') as w:
            w.write(r.content)


movies = read_jsons_to_arrays()
add_num_of_movies("actor", "Actors")
add_num_of_movies("director","Directors")
add_num_of_movies("director","Producers")