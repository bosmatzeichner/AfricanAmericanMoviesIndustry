import numpy as np
import json
import http.client
import time

def openJsonFile(name):
    with open(name) as json_file:
        return json.load(json_file)

def getFiles(filesToOpen):
    arrays = []
    for name in filesToOpen:
        arrays.append(openJsonFile("./PeopleArrays"+name+".json"))
    return arrays

def getArrays(files, arrayName):
    arrays = []
    for file in files:
        arrays.append(file[arrayName])
    return arrays

def mergeArrays(arrays):
    merged = [0] * 2370000
    for array in arrays:
        if(len(array) < 2370000):
            tmpArr = [0] * (2370000 - len(array))
            array.extend(tmpArr)
        merged = np.logical_or(merged, array)
    merged = np.ndarray.tolist(merged)
    return merged


filesToOpen = ["19391969","19691989","19892001","20012007","20072011","20112014","20142017","20172019"]
files = getFiles(filesToOpen)

actors_arrays = getArrays(files, "actorsArray")
actorsArray = mergeArrays(actors_arrays)

directors_arrays = getArrays(files, "directorsArray")
directorsArray = mergeArrays(directors_arrays)

producers_arrays = getArrays(files, "producersArray")
producersArray = mergeArrays(producers_arrays)


# last_index  = len(actorsArray)-1-actorsArray[::-1].index(True)
# print("last index:", last_index)

# dataFile = open("merged.json", "a")
# dict = {"actorsArray": actorsArray, "directorsArray": directorsArray, "producersArray": producersArray}
# dataFile.write(json.dumps(dict))
# with open("./merged.json") as json_file:
#     dic = json.load(json_file)
#     actorsArray = dic["actorsArray"]
#     directorsArray = dic["directorsArray"]
#     producersArray = dic["producersArray"]
counter = 0
def getDataStr(i):
    global counter
    counter +=1
    print("counter is:" ,counter)
    if(counter % 40 == 0 ):
        time.sleep(10)
    payload = "{}"
    req = "https://api.themoviedb.org/3/person/%d?api_key=5c1eeb331ccdc877d96b634737ed2560&language=en-US" % (i)
    conn.request("GET", req, payload)
    res = conn.getresponse()
    print("res is: " ,res.status)
    data = res.read()
    data = data.decode("utf-8")
    print("data is,", data)
    return data

def addPersonIfTrue(array, i, toAdd, datastr):
    if array[i] == True:
        if datastr == '{"status_code":34,"status_message":"The resource you requested could not be found.","success":false}':
            return -1
        parsed = json.loads(datastr)
        toAdd.append(parsed)
        return 1
    return 0

actors = []
directors = []
producers = []
with open("./actorsData1.json") as json_file:
    actorsData3 = json.load(json_file)
with open("./directorsData1.json") as json_file:
    directorsData3 = json.load(json_file)
with open("./producersData1.json") as json_file:
    producersData3 = json.load(json_file)

last_index = len(actorsData3)
print("last index:", last_index)
if(last_index<len(directorsData3)):
    last_index = len(directorsData3)-1
if(last_index<len(producersData3)):
    last_index = len(producersData3)-1
conn = http.client.HTTPSConnection("api.themoviedb.org")
i = 0

def getIds (data, array_ids):
    for item in data:
        if ('status_code' in item):
            continue
        id = item['id']
        array_ids.append(id)
    return array_ids


def getRest(array,start,end, toPrint,array_ids,toAdd):
    for index in range(start, end + 1):
        if (array[index] == False):
            continue
        if (index in array_ids):
            continue
        data = getDataStr(index)
        print(toPrint)
        toAdd.append(data)

actors_ids = getIds(actorsData3 , [])
directors_ids = getIds(directorsData3 , [])
producers_ids = getIds(producersData3 , [])

# getRest(actorsArray ,actors_ids[0], actors_ids[len(actors_ids) -1], "added actor", actors_ids,actors)
#
# dataFileActors = open("./actorsData1rest.json", "a")
# dataFileActors.write(json.dumps(actors, indent=4))
#
# getRest(directorsArray,directors_ids[0], directors_ids[len(directors_ids) - 1], "added director",directors_ids,directors)
#
# dataFileDirectors = open("./directorsData1rest.json", "a")
# dataFileDirectors.write(json.dumps(directors, indent=4))

getRest(producersArray,producers_ids[0], producers_ids[len(producers_ids)-1], "added producer",producers_ids,producers)

dataFileProducers = open("./producersData1rest.json", "a")
dataFileProducers.write(json.dumps(producers, indent=4))

print("done")