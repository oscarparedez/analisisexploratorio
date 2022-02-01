import pandas as pd
import scipy
import numpy as np
import matplotlib.pyplot as plt
from pandasql import sqldf
pd.set_option('display.max_columns', None)

movies = pd.read_csv('movies.csv', encoding='cp1252')
#print(movies.describe())

cuantitativas = ['budget', 'revenue', 'runtime', 'genresAmount', 'productionCoAmount', 'productionCountriesAmount', 'voteCount', 'voteAvg', 'actorsAmount']
cuantitativasEspeciales = ['actorsPopularity']
cuantitativasConErrores = ['castWomenAmount', 'castMenAmount']
cualitativas = ['id', 'popularity', 'originalTitle', 'originalLanguage', 'title', 'homePage', 'video', 'releaseDate']
cualitativasEspeciales = ['genres', 'productionCompany', 'productionCompanyCountry', 'productionCountry']
    
for col in cuantitativas:
    movies.hist(column=col)

for col in cuantitativasConErrores:
    newArray = [i for i in movies[col].to_numpy() if i.isnumeric()]
    plt.hist(newArray, bins="auto")
    plt.show()
    
for col in cuantitativasEspeciales:
    df = pd.DataFrame(movies[col].str.split('|', expand=True).stack().value_counts())
    df.hist(column=0, bins=np.linspace(0,120))
    plt.suptitle(col)
    
""" for col in cualitativasEspeciales:
    elementCount = {}
    for element in movies[col]:
        element = str(element)
        elementList = element.split('|')
        for single in elementList:
            if not (single in elementCount):
                elementCount[single] = 1
            else:
                elementCount[single] = elementCount[single] + 1
    print(pd.DataFrame(elementCount, index=[0])) """
for col in cualitativasEspeciales:
    df = pd.DataFrame(movies[col].str.split('|', expand=True).stack().value_counts())
    print(df)

movies.sort_values(by='budget', ascending=False)[['originalTitle','budget']].head(10)
movies.sort_values(by='revenue', ascending=False)[['originalTitle','revenue']].head(10)
movies.sort_values(by='voteCount', ascending=False)[['originalTitle','voteCount']].head(1)
movies.sort_values(by='voteCount', ascending=True)[['originalTitle','voteCount']].head(1)

output = sqldf("select strftime('%Y', releaseDate) as Year, Count(releaseDate) as RECUENTO from movies Group By Year Order by RECUENTO DESC")
print(output)
output = sqldf("select * from output limit 10")
plt.hist(output.Year, weights=output.RECUENTO)

output = sqldf("select *  from movies Order by releaseDate DESC limit 20")
df = pd.DataFrame(output["genres"].str.split('|', expand=True).stack().value_counts())
df.columns = ["cookie"]
df["genres"] = list(df.index)
print(df)
plt.hist(df.genres, weights=df.cookie)
plt.xticks(rotation='vertical')
plt.show()

output = sqldf("select genres, (revenue - budget) as GANANCIAS from movies Group By genres Order by GANANCIAS DESC")
leng = len(output.genres.str.split('|'))
generos = []
for i in range(leng):
    if output.genres.str.split('|')[i] != None: 
        generos.append(output.genres.str.split('|')[i][0])
    else:
        generos.append("None")
output = output.assign(genres=generos)
output = sqldf("select genres, SUM(GANANCIAS) As SUMA from output group by genres order by SUMA DESC")
#output = output.explode("genres")
#output = sqldf("select genres, SUM(GANANCIAS) from output Group By genres Order by GANANCIAS DESC")
print(output)