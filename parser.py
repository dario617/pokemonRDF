import os


def saveRDF(thePokes, cols):
    rdfFile = open('pokeParsed.ttl','w')

    # Write headers
    rdfFile.write("@prefix : <http://example.org> .\n")
    rdfFile.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.\n")
    rdfFile.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n\n")

    for i in range(len(thePokes)):
        # Get the name and create the pokemon
        fixedName = thePokes[i]['name'].lower().replace(" ","-").replace("é","e").replace("'","")
        formatedLine = "<https://pokemondb.net/pokedex/{0}> a :Pokemon".format(fixedName)
        if thePokes[i]['is_legendary'] == '1':
            formatedLine += ",Legendary;\n"
        else:
            formatedLine += ";\n"

        # Put habilites
        for j in range(len(thePokes[i]['abilities'])):
            formatedLine += "\t :hasHability \"{0}\";\n".format(thePokes[i]['abilities'][j])
        
        # Normal stats
        for j in range(1,24):
            formatedLine += "\t :{0} \"{1}\"^^xsd:decimal;\n".format(cols[j],thePokes[i][cols[j]])
        for j in range(25,29):
            if j == 26 and thePokes[i]['experience_growth'] != '':
                formatedLine += "\t :{0} \"{1}\"^^xsd:decimal;\n".format(cols[j],thePokes[i][cols[j]])
            else:
                formatedLine += "\t :{0} \"{1}\"^^xsd:decimal;\n".format(cols[j],thePokes[i][cols[j]])
        for j in range(33,36):
                formatedLine += "\t :{0} \"{1}\"^^xsd:decimal;\n".format(cols[j],thePokes[i][cols[j]])
        formatedLine += "\t :weight_kg \"{0}\"^^xsd:decimal;;\n".format(thePokes[i]['weight_kg'])

        # Classifications
        formatedLine += "\t :classification \"{0}\";\n".format(thePokes[i]['classfication'].replace("é","e"))
        if thePokes[i]['type1'] != '':
            formatedLine += "\t :pokeType \"{0}\";\n".format(thePokes[i]['type1'])
        if thePokes[i]['type2'] != '':
            formatedLine += "\t :pokeType \"{0}\";\n".format(thePokes[i]['type2'])
        formatedLine += "\t :generation \"{0}\"^^xsd:int;\n".format(thePokes[i]['generation'])
        formatedLine += "\t :pokedexNumber \"{0}\"^^xsd:int;\n".format(thePokes[i]['pokedex_number'])
        formatedLine += "\t :image <https://img.pokemondb.net/artwork/{0}.jpg>.\n\n".format(fixedName)

        rdfFile.write(formatedLine)

    rdfFile.close()

def parseHabilites(line):

    habilities_raw = line.split("]")[0][2:].replace("'","").split(",")
    for i in range(len(habilities_raw)):
        habilities_raw[i] = habilities_raw[i].strip()
    return habilities_raw

def parsePokemon():
    pokeFile = open("pokemon.csv",'r', encoding="utf-8")
    pokemons = list()
    columns = pokeFile.readline()[:-1].split(',')
    line = pokeFile.readline()
    while line:
        #Get attributes
        line = line[:-1]
        habilities = parseHabilites(line)
        aPokemon = line.split(']')[1].split(",")
        dictPokemon = dict()
        dictPokemon['abilities'] = habilities

        for i in range(1,len(columns)):
            dictPokemon[columns[i]] = aPokemon[i]
        pokemons.append(dictPokemon)

        line = pokeFile.readline()

    pokeFile.close()
    return pokemons, columns

def csvToRDF():
    pokemonlist, cols = parsePokemon()
    saveRDF(pokemonlist, cols)

if __name__ == "__main__":
    csvToRDF()