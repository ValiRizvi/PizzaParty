from utils.geo_store_locator import getCoordinates

from pizza_chains.dominos import scrapeDominos, getDominosStoreID
from pizza_chains.pizzapizza import scrapePizzaPizza, getPizzaPizzaStoreID
from pizza_chains.papajohns import scrapePapaJohns

# if foundAStore returns as false then we know there are no stores nearby from any one of the chains.
def scrapeStores(postalCode: str):
    foundAStore = False

    coordinates = getCoordinates(postalCode)

    dominosStoreID = getDominosStoreID(coordinates)
    if isinstance(dominosStoreID, int):  # if store ID is an integer that means a store was found so we proceed to scrape it
        scrapeDominos(dominosStoreID)
        foundAStore = True


    pizzapizzaStoreID = getPizzaPizzaStoreID(coordinates)
    if isinstance(pizzapizzaStoreID, int):
        scrapePizzaPizza(pizzapizzaStoreID)
        foundAStore = True


    if isinstance(scrapePapaJohns(postalCode), int):
        foundAStore = True


    return foundAStore