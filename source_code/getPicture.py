import requests
import json


with open("./AfricanAmericanDirectors/africanAmericanDirectorsData.json") as json_file:
    data = json.load(json_file)
sortedData = sorted(data,reverse=True, key = lambda i: i['popularity'])

dataFileSortedDirectors = open("./SortedAfricanAmericanDirectors.json", "a")
dataFileSortedDirectors.write(json.dumps(sortedData, indent=4))

mostPopular = sortedData[:10]
dataFileMostPopular = open("./top10Directors.json", "a")
dataFileMostPopular.write(json.dumps(mostPopular, indent=4))

base_url = "http://image.tmdb.org/t/p/"
size = "w185"
for item in mostPopular:
    name = item['name']
    path = item['profile_path']
    url = base_url+size+path
    r = requests.get(url)
    filetype = r.headers['content-type'].split('/')[-1]
    filename = 'poster_{0}.{1}'.format(name,filetype)
    with open(filename,'wb') as w:
        w.write(r.content)