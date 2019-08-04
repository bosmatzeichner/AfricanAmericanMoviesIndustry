import json
import requests

def read_jsons_to_arrays():
    yearsArray = ["19391969", "19691989","19892001", "20012007","20072011", "20112014","20142017", "20172019"]
    movies_res = []
    for years in yearsArray:
        path = './MoviesDataWithBlackActors/moviesWith'+years+'BlackActors.json'
        with open(path) as json_file:
            movies_res.extend(json.load(json_file))
    # print ("num of movies is: ",len(movies))
    return movies_res


def add_num_of_movies(actors):
    africanAmericanActorsPath = "./AfricanAmerican"+actors+"./africanAmerican"+actors+"Data.json"
    with open(africanAmericanActorsPath) as json_file:
        blackActors = json.load(json_file)

    for actor in blackActors:
        actor['numOfMovies'] = 0
    for actor in blackActors:
        for movie in movies:
            for record in movie['BlackActors']:
                if actor['id'] == record['id']:
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
        path = item['profile_path']
        url = base_url + size + path
        r = requests.get(url)
        filetype = r.headers['content-type'].split('/')[-1]
        filename = 'poster_{0}.{1}'.format(name, filetype)
        with open(filename, 'wb') as w:
            w.write(r.content)


movies = read_jsons_to_arrays()
add_num_of_movies("Actors")
add_num_of_movies("Directors")
add_num_of_movies("Producers")