
import json

def mergeJsons(firstData,secondData,thirdData):
    new_data = []
    data = firstData+ secondData + thirdData
    for item in data:
        if ('status_code' in item):
            continue
        else:
            new_data.append(item)
    open("./africanAmericanProducersData.json","w").write(json.dumps(new_data, indent=4))

def openJsonFile(name):
    with open(name) as json_file:
        return json.load(json_file)

def mergeEach3Jsons(files):
    data1 = openJsonFile("./"+files[0]+".json")
    data2 = openJsonFile("./"+files[1]+".json")
    data3 = openJsonFile("./" + files[2] + ".json")
    mergeJsons(data1,data2,data3)

files = ["producersData1AfricanAmerican","producersData2AfricanAmerican","producersData3AfricanAmerican"]
mergeEach3Jsons(files)