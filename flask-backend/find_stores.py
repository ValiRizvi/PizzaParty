from geo_store_locator import getDominosStoreID, getPizzaPizzaStoreID

from pizza_chains.dominos import scrapeDominos
from pizza_chains.pizzapizza import scrapePizzaPizza
from pizza_chains.papajohns import scrapePapaJohns

def findStores(postalCode):
    foundAStore = False

    dominosStoreID = getDominosStoreID(postalCode)
    if not isinstance(dominosStoreID, str):
        scrapeDominos(dominosStoreID)
        foundAStore = True

    pizzapizzaStoreID = getPizzaPizzaStoreID(postalCode)
    if not isinstance(pizzapizzaStoreID, str):
        scrapePizzaPizza(pizzapizzaStoreID)
        foundAStore = True

    if not isinstance(scrapePapaJohns(postalCode), str):
        foundAStore = True

    return foundAStore