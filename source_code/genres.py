
import http.client
import json
conn = http.client.HTTPSConnection("api.themoviedb.org")

genresArr = {}
payload = "{}"

conn.request("GET", "/3/genre/movie/list?language=en-US&api_key=5c1eeb331ccdc877d96b634737ed2560", payload)

res = conn.getresponse()
data = res.read()
parsed = json.loads(str(data.decode("utf-8")))
genres = parsed["genres"]
print ("num of genres is: ",len(genres))
for genre in genres:
    print(genre)
    genresArr[genre['id']] = genre['name']
print (genresArr)
groupsArray = ["Actors", "Directors", "Producers"]
yearsArray = ["19391969" ,"19691989", "19892001", "20012007",
              "20072011", "20112014", "20142017", "20172019"]

def read_jsons_to_arrays():
    movies = []
    for years in yearsArray:
        path = './MoviesDataWithBlackActors/moviesWith'+years+'BlackActors.json'
        with open(path) as json_file:
            movies.extend(json.load(json_file))
    print ("num of movies is: ",len(movies))
    return movies

# nameOfGroup = actors/directors/producers
def get_genres(movies, nameOfGroup):
    genres = {}
    group = "Black"+nameOfGroup
    group_sum = "numOf"+group
    for m in movies:
        genre_ids = m["genre_ids"]
        if genre_ids:
            for _id_ in genre_ids:
                if _id_ in genres:
                    genres[_id_]['numOfMovies'] += 1
                    num_of_people1 = len(m[group])
                    num_of_people2 = len(m[nameOfGroup])
                    genres[_id_][group_sum] += num_of_people1
                    genres[_id_]['numOf'+nameOfGroup] += num_of_people2
                    # d2 = [{'title': m['title'],'release_date': m['release_date'], group: m[group]}]
                    # genres[_id_]['movies'].extend(d2)

                else:
                    num_of_people1 = len(m[group])
                    num_of_people2 = len(m[nameOfGroup])
                    d1 = {_id_: { 'genre': genresArr[_id_] ,'genreId': _id_, 'movies ratio': 0, 'black ratio': 0 ,'averageOf'+group: 0, 'averageOf'+nameOfGroup: 0,  'numOfMovies': 1, group_sum: num_of_people1, 'numOf'+nameOfGroup: num_of_people2,
                                  'numOf'+nameOfGroup: num_of_people2
                                  # }}
                                  ,'movies': [ {'title': m["title"], 'release_date': m["release_date"], group: m[group]}]}}
                    genres.update(d1)
    for genre in genres:
        # print("genre: ",genres[genre])
        num_of_movies = genres[genre]["numOfMovies"]
        num_of_black_people = genres[genre][group_sum]
        num_of_people = genres[genre]['numOf'+nameOfGroup]
        average_black = num_of_black_people/num_of_movies
        average_num_of_people = num_of_people/num_of_movies
        genres[genre]['averageOf'+group] = average_black
        genres[genre]['averageOf'+nameOfGroup] = average_num_of_people
        black_ratio = average_black/average_num_of_people
        movies_ratio = genres[genre]['numOfMovies']/len(movies)
        genres[genre]['black ratio'] = black_ratio*100
        print("genre is: ", genres[genre]['genre'])
        print("average of black: ",genres[genre]['averageOf'+group])
        print("average of actors: ",genres[genre]['averageOf'+nameOfGroup])
        print("ratio of black: ",genres[genre]['black ratio'])

        genres[genre]['movies ratio'] = movies_ratio*100
    return genres


movies = read_jsons_to_arrays()
# movies_with_directors = read_jsons_to_arrays()
# movies_with_producers = read_jsons_to_arrays()


def change_to_legal_json(genres):
    a = []
    for genre in genres:
        a.extend([genres[genre]])
    return a


actorsMoviesGenres = get_genres(movies, "Actors")
open("./actorsMoviesGenres.json", "w").write(json.dumps(change_to_legal_json(actorsMoviesGenres), indent=4))

directorsMoviesGenres = get_genres(movies, "Directors")
open("./directorsMoviesGenres.json", "w").write(json.dumps(change_to_legal_json(directorsMoviesGenres), indent=4))

producersMoviesGenres = get_genres(movies, "Producers")
open("./producersMoviesGenres.json", "w").write(json.dumps(change_to_legal_json(producersMoviesGenres), indent=4))
