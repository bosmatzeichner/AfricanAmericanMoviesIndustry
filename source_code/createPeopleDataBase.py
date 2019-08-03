import numpy as np
import json
import http.client

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
# list1 = [ elem for elem in actorsArray if elem is True]
# print(len(list1))


# with open('actorsData2.json') as json_file:
#     data = json.load(json_file)
# id_array = []
# for item in data:
#     if ('status_code' in item):
#         continue
#     id = item['id']
#     id_array.append(id)
# print(id_array)
# for i in range(1000061,1699979):
#     if(actorsArray[i] == True):
#         if(not i in id_array):
#             print(i)
# print("done")



directors_arrays = getArrays(files, "directorsArray")
directorsArray = mergeArrays(directors_arrays)

producers_arrays = getArrays(files, "producersArray")
producersArray = mergeArrays(producers_arrays)

last_index  = len(actorsArray)-1-actorsArray[::-1].index(True)
print("last index:", last_index)

# dataFile = open("merged.json", "a")
# dict = {"actorsArray": actorsArray, "directorsArray": directorsArray}
# dataFile.write(json.dumps(dict))

conn = http.client.HTTPSConnection("api.themoviedb.org")


def getDataStr(i):
    payload = "{}"
    req = "https://api.themoviedb.org/3/person/%d?api_key=5c1eeb331ccdc877d96b634737ed2560&language=en-US" % (i)
    conn.request("GET", req, payload)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

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
for i in range(1000000 , 1700000): #49618
    print(i)
    datastr=""
    if(actorsArray[i] and directorsArray[i] and producersArray[i]):
        datastr = getDataStr(i)
    elif actorsArray[i] and directorsArray[i]:
        datastr = getDataStr(i)
    elif actorsArray[i] and producersArray[i]:
        datastr = getDataStr(i)
    elif directorsArray[i] and producersArray[i]:
        datastr = getDataStr(i)
    elif directorsArray[i]:
        datastr = getDataStr(i)
    elif actorsArray[i]:
        datastr = getDataStr(i)
    elif producersArray[i]:
        datastr = getDataStr(i)

    res = addPersonIfTrue(actorsArray, i, actors,datastr)
    if(res == -1):
        continue
    if(res == 1):
        print("added actor")
    res = 0
    res = addPersonIfTrue(directorsArray, i, directors,datastr)
    if (res == -1):
        continue
    if (res == 1):
        print("added director")
    res = 0
    res = addPersonIfTrue(producersArray, i, producers,datastr)
    if (res == -1):
        continue
    if (res == 1):
        print("added producer")
    res = 0

dataFileActors = open("./actorsData2.json", "a")
dataFileActors.write(json.dumps(actors, indent=4))

dataFileDirectors = open("./directorsData2.json", "a")
dataFileDirectors.write(json.dumps(directors, indent=4))

dataFileProducers = open("./producersData2.json", "a")
dataFileProducers.write(json.dumps(producers, indent=4))

