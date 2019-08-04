# AfricanAmericanMoviesIndustry

Creating data bases:

	Source data from IMDB:
		
		All movies from 1939-2019 - json files - getMovies.py
		
		All movies with cast and crew members - addCastToMovies.py
		
		All actors / producers / directors - json files - getPeopleNew.py (binary arrays) -> createPeopleDataBase.py (import by values of mreged array)

	Steps:
		1. Ceating data base of movies from 1939 to 2019.
		
		2. Creating binary lists for actors/directors/producers where the index is the id of the person and the value in any cell is 1 if the person took a part of a movie these years. Finally, merged all people arrays.
		
		3. Creating data base based on imported data for each person that we found over the 80 years.

Filtering data:

	Filtered Data:
	
		All African-American actors/directors/producers dataBase - getBlackPeopleNew.py
		
		All movies that contain at least one African-American actor/director/producer - addCastToMovies.py		
	
	Steps:
		1. Filter people data base by African American ethnic group, using wikidata (extract list of African-American actors/directors/producers and store the relevant people). Adding qnumber field to each of them. 
	
		2. Filter movies data base by movies that contain at least one African American actor which is in the filtered data "African American actors/directors/producers ". Adding fields of the African American actors/directors/producers to each movie.

Processing data:
	
	MOVIES:
	
		How many movies per year. Adding dictionary per year that contains: {year = number, moviescounter = number, moviesid = list of numbers}.
		
		How many movies with at least 1 African American person per year and the percentage/ratio of them?
		
		How many African American people per year?
		
		How many female/male are there? -
		
		Count number of movies and number of African American actors/directors/producers per genre. - genres
		
		Find occupations of characters played by black actors and rate them by the counter that we save for each job. - occupationsNew.py
	
	PEOPLE:
	
		
		How many of the people in the filtered data are male/female.
		
		Creating a map of place of birth areas.
		
		popularity - for each person find out in how many movies he took place.
		
		map the places of birth.
        

