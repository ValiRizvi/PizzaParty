from utils.geo_store_locator import getCoordinates

from pizza_chains.dominos import scrapeDominos, getDominosStoreID
from pizza_chains.pizzapizza import scrapePizzaPizza, getPizzaPizzaStoreID
from pizza_chains.papajohns import scrapePapaJohns, getPapaJohnsStoreID

from firestore_client import checkStoreScrapedToday

# if foundAStore returns as false then we know there are no stores nearby from any one of the chains.
def scrapeStores(postalCode: str):

    notFound = 0

    coordinates = getCoordinates(postalCode)

    notFound += scrape('Dominos', getDominosStoreID, scrapeDominos, coordinates) # returns 1 if store data collected, 0 if not
    notFound += scrape('PizzaPizza', getPizzaPizzaStoreID, scrapePizzaPizza, coordinates)
    notFound += scrape('PapaJohns', getPapaJohnsStoreID, scrapePapaJohns, postalCode)

    if notFound == 3:
        return False # no store data available for all chains

    return True # data for at least one store is available



def scrape(chain_collection_name: str, getStoreId: callable, scrapeFunction: callable, locationInfo: str | dict):

    storeId = getStoreId(locationInfo)

    if isinstance(storeId, int): # if store ID is an integer that means a store was found so we proceed to scrape it
        if not checkStoreScrapedToday(chain_collection_name, str(storeId)):
            scrapeFunction(storeId)
    else:
        return 1 # store not found
    
    return 0 # store scraped successfully

