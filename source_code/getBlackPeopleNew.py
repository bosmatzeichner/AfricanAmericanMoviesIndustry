import json

from SPARQLWrapper import SPARQLWrapper, JSON


def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def create_african_american_json(african_americans):
    query = """SELECT DISTINCT ?name ?nameLabel ?occLabel WHERE {
  ?name wdt:P172 wd:Q49085.
  VALUES (?occ) { (wd:Q33999) (wd:Q10800557) (wd:Q2526255) (wd:Q3282637) (wd:Q21169216) (wd:Q578109) (wd:Q2059704) (wd:Q10798782)}.
  ?name wdt:P106 ?occ.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
 }  """
    endpoint_url = "https://query.wikidata.org/sparql"
    results = get_results(endpoint_url, query)
    print("--------------start query for african american people:")
    for result in results["results"]["bindings"]:
        person = {}
        name = result['nameLabel']['value']
        QNumber = result['name']['value']
        QNumber = QNumber.rsplit('/')[-1]
        person["name"] = name
        person["Qnumber"] = QNumber
        print(person)
        african_americans.append(person)

    print("--------------creating json file: africanAmericanPeople.json")
    open("./" + "africanAmericanPeople.json", "w").write(json.dumps(african_americans, indent=4))


def open_json_file(name):
    with open(name) as json_file:
        return json.load(json_file)


def filter_non_african_american_people(files,african_americans):
    print("---------------------------start to filter!-------------------------")
    for file_name in files:
        print("-----------------filtering ",file_name)
        AfricanAmericansInFile = []
        data = open_json_file("./"+file_name+"New.json")
        for person in data:
            for p in african_americans:
                if (person["name"] == p["name"]):
                    person["Qnumber"] = p["Qnumber"]
                    AfricanAmericansInFile.append(person)
                    print ("added "+ person["name"])
                    break
        print("--------done filtering "+ file_name)
        print("---------------creating json file: "+ file_name+"AfricanAmerican.json")
        open("./" +file_name+"AfricanAmerican.json", "w").write(json.dumps(AfricanAmericansInFile, indent=4))


def get_black_people_new():
    african_americans = []
    create_african_american_json(african_americans)
    files = ["actorsData1","directorsData1","producersData1"]
    filter_non_african_american_people(files,african_americans)


get_black_people_new()