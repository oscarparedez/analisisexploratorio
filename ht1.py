import pandas as pd

pd.set_option('display.max_columns', None)

movies = pd.read_csv('movies.csv', encoding='cp1252')
#print(movies.describe())

cuantitativas = ['budget', 'revenue', 'runtime', 'genresAmount', 'productionCoAmount', 'productionCountriesAmount', 'voteCount', 'voteAvg', 'actorsPopularity', 'actorsAmount', 'castWomenAmount', 'castMenAmount']
cualitativas = ['id', 'popularity', 'originalTitle', 'originalLanguage', 'title', 'homePage', 'video', 'releaseDate']
cualitativasEspeciales = ['genres', 'productionCompany', 'productionCompanyCountry', 'productionCountry']

#for col in cualitativas:
#    print(movies[col].value_counts())
    
for col in cualitativasEspeciales:
    elementCount = {}
    for element in movies[col]:
        element = str(element)
        elementList = element.split('|')
        for single in elementList:
            if not (single in elementCount):
                elementCount[single] = 1
            else:
                elementCount[single] = elementCount[single] + 1
    print(pd.DataFrame(elementCount, index=[0]))

    
    