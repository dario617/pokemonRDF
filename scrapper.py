from bs4 import BeautifulSoup
import requests

# File URL LIST
def putEvolution(aSet,target):
    for i in range(1,len(target)):
        el1 = target[i-1].text.lower()
        el2 = target[i].text.lower()
        line = "<https://pokemondb.net/pokedex/{0}> :evolvesInto <https://pokemondb.net/pokedex/{1}>.\n".format(el1,el2)
        if line not in aSet:
            aSet.add(line)

def putEvolutionOrigin(aSet,origin,target):

    # Check that the target has no intermediate evolutions
    for i in range(len(target)):

        intraEvolutions = target[i].find_all("a",{"class": "ent-name"})

        el = intraEvolutions[0].text.lower()
        line = "<https://pokemondb.net/pokedex/{0}> :evolvesInto <https://pokemondb.net/pokedex/{1}>.\n".format(origin.text.lower(),el)
        if line not in aSet:
            aSet.add(line)

        for j in range(1,len(intraEvolutions)):
            el1 = intraEvolutions[j-1].text.lower()
            el2 = intraEvolutions[j].text.lower()
            line = "<https://pokemondb.net/pokedex/{0}> :evolvesInto <https://pokemondb.net/pokedex/{1}>.\n".format(el1,el2)
            if line not in aSet:
                aSet.add(line)
    
def writeToTTL(TTL,aSet):
    # Clear set
    for el in aSet:
        #print("Putting "+str(el.encode("utf-8"))+ " \n")
        sp = el.split(" :evolvesInto ")
        if sp[0] != sp[1][:-2]:
            try:
                TTL.write(el)
            except Exception:
                print("Couldn't write"+el)
    TTL.flush()

def getEvolutions():
    pokeURLs = open("URLS.txt",'r')
    pokemonTTL = open("pokeParsed.ttl",'a',encoding="utf-8")

    evolutionSet = set()
    line = pokeURLs.readline()
    while line:
        print("Getting "+line[:-1])
        current = line[:-1]
        #current = "https://pokemondb.net/pokedex/cosmog"
        r = requests.get(current)
        soup = BeautifulSoup(r.text, 'html.parser')

        if "404" in soup.find_all("title")[0].text:
            print("\n404 error\n")

        things = soup.find_all("div",{"class": 'infocard-list-evo'})
        if len(things) != 0:
            # Got evolutions
            evolutions_div = things[0].find_all("a",{"class": "ent-name"})

            evolutions_optional = things[0].find_all("span",{"class":"infocard-evo-split"})

            if len(evolutions_optional) != 0:
                evolutions_optional = evolutions_optional[0].find_all("a",{"class": "ent-name"})
                # Get the first ones
                directEvolutions = [i for i in evolutions_div + evolutions_optional if i not in evolutions_div or i not in evolutions_optional]
                putEvolution(evolutionSet,directEvolutions)

                # Get the new lists
                bif = evolutions_optional = things[0].find_all("span",{"class":"infocard-evo-split"})[0].find_all("div",{"class": "infocard-list-evo"})
                putEvolutionOrigin(evolutionSet,directEvolutions[-1],evolutions_optional)
            else:
                putEvolution(evolutionSet,evolutions_div)

        else:
            print("no evolutions for "+current)
        line = pokeURLs.readline()

    writeToTTL(pokemonTTL,evolutionSet)

    pokemonTTL.close()
    pokeURLs.close()

if __name__ == "__main__":
    getEvolutions()