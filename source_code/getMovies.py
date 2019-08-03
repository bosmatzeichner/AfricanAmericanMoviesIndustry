import http.client
import json
import time

def getPages(releaseDateGte, releaseDateLte):
    conn = http.client.HTTPSConnection("api.themoviedb.org")
    pages = []
    for i in range(1,1001):
        if i%40 == 0:
            time.sleep(10)
        payload = "{}"
        req = "/3/discover/movie?release_date.lte=%s&release_date.gte=%s&primary_release_date.lte=%s&primary_release_date.gte=%s&page=%d&include_video=false&include_adult=false&sort_by=release_date.asc&region=US&language=en-US&api_key=5c1eeb331ccdc877d96b634737ed2560" %(releaseDateLte, releaseDateGte,releaseDateLte,releaseDateGte, i)
        conn.request("GET",req , payload)
        res = conn.getresponse()
        data = res.read()
        datastr = str(data.decode("utf-8"))
        pages.append(datastr)

    return pages


pages = getPages("2017-01-02", "2019-01-01")
# pages.extend(getPages("1969-01-02", "1989-01-01"))
# pages.extend(getPages("1989-01-02", "2001-01-01"))
# pages.extend(getPages("2001-01-02", "2007-01-01"))
# pages.extend(getPages("2007-01-02", "2011-01-01"))
# pages.extend(getPages("2011-01-02", "2014-01-01"))
# pages.extend(getPages("2014-01-02", "2017-01-01"))
# pages.extend(getPages("2017-01-02", "2019-01-01"))
dataFile = open("./movieData20172019.json", "a")
`

#parsing json
