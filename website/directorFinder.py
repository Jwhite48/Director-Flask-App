import requests
import json
from collections import Counter

tmdb_key = ''
img_baseURI = 'https://image.tmdb.org/t/p/w500'

def getDirector(directorName):
    directorQuery = 'https://api.themoviedb.org/3/search/person?api_key='\
                    + tmdb_key + '&language=en-US&query=' + directorName + '&page=1&include_adult=false'
    requestObj = requests.get(directorQuery)
    json_data = json.loads(requestObj.text)
    results = json_data['results']

    ret = []
    for result in results:
        directed_movies = []

        personQuery = 'https://api.themoviedb.org/3/person/'\
                      + str(result['id']) + '/movie_credits?api_key=' + tmdb_key + '&language=en-US'
        requestObj = requests.get(personQuery)
        json_data = json.loads(requestObj.text)
        for movie in json_data['crew']:
            if movie['department'].lower() == 'directing' and movie['job'].lower() == 'director':
               directed_movies.append(movie)

        directed_movies.sort(key=lambda x: x['popularity'], reverse=True)
        if len(directed_movies) == 0: continue
        while len(directed_movies) > 10:
            directed_movies.pop()

        
        movies = []
        for movie in directed_movies:
            mv = {}
            mv['title'] = movie['title'] + ' (' + \
                          (movie['release_date'].split('-',1)[0] if len(movie['release_date']) > 0 else 'N/A') + ')'
            mv['id'] = str(movie['id'])
            movies.append(mv)

        x = {}
        x['name'] = result['name']
        x['picture'] = img_baseURI + result['profile_path'] if result['profile_path'] else ''
        x['movies'] = movies
        x['id'] = result['id']

        ret.append(x)

    return ret

def similarDirectors(movies, directorName):
    directorRecs = []

    for id in movies:
        #Check if equestObj is 404 or not
        reccQuery = 'https://api.themoviedb.org/3/movie/' + str(id) + '/recommendations?api_key=' + tmdb_key + '&language=en-US&page=1'
        requestObj = requests.get(reccQuery)
        json_data = json.loads(requestObj.text)
        results = json_data['results']
        for recMovie in results:
            directorQuery = 'https://api.themoviedb.org/3/movie/' + str(recMovie['id']) + '/credits?api_key=' + tmdb_key + '&language=en-US'
            requestObj = requests.get(directorQuery)
            json_data = json.loads(requestObj.text)
            crew = json_data['crew']

            directorRecs += [{'name': member['name'],
                              'picture': img_baseURI+str(member['profile_path']),
                              'link': 'https://themoviedb.org/person/'+str(member['id'])} 
                              for member in crew if member['name'].lower() != directorName.lower() and member['job'].lower() == 'director']    
    
    c = (Counter(json.dumps(l) for l in directorRecs)).most_common(5)
    for i in range(len(c)):
        c[i] = list(c[i])
        c[i][0] = json.loads(c[i][0])
        c[i][0]['score'] = c[i][1]
        c[i].pop()
    c = [item for items in c for item in items]
    return c