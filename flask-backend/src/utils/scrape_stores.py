from utils.geo_store_locator import getCoordinates

from pizza_chains.dominos import scrapeDominos, getDominosStoreID
from pizza_chains.pizzapizza import scrapePizzaPizza, getPizzaPizzaStoreID
from pizza_chains.papajohns import scrapePapaJohns, getPapaJohnsStoreID

from utils.firestore_client import checkStoreScrapedToday


def scrapeStores(postalCode: str):

    local_stores = {}

    coordinates = getCoordinates(postalCode)

    scrape('Dominos', getDominosStoreID, scrapeDominos, coordinates, local_stores)
    scrape('PapaJohns', getPapaJohnsStoreID, scrapePapaJohns, postalCode, local_stores)
    scrape('PizzaPizza', getPizzaPizzaStoreID, scrapePizzaPizza, coordinates, local_stores)

    return local_stores # dict of local stores, will be empty if no stores are nearby



def scrape(chain_collection_name: str, getStoreId: callable, scrapeFunction: callable, locationInfo: str | dict, local_stores: dict):

    storeId = getStoreId(locationInfo)

    if isinstance(storeId, int): # if store ID is an integer that means a store was found 
        # if the store was already scraped today no need to scrape again 
        if not checkStoreScrapedToday(chain_collection_name, str(storeId)):
            scrapeFunction(storeId)
        
        # store the id in dict to have a log of relevant stores to later query from db and retrieve relevant coupons
        local_stores[chain_collection_name] = str(storeId)



