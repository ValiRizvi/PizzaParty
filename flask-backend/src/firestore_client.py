import os 
from google.cloud import firestore
from datetime import datetime

firebase_credentials = os.getenv("FIREBASE_ADMIN_CREDENTIALS")

db = firestore.Client.from_service_account_json(firebase_credentials)

currentTime = datetime.now()
date = currentTime.date()


def addCouponsToDB(chain_name: str, store_id: str, coupons: list):

    deleteCoupons(chain_name, store_id) # delete outdated coupons if they exist

    try:
        coupon_batch = db.batch() # batch coupon writes together for efficiency
        collection_ref = db.collection(chain_name) # create collection for each chain
        store_ref = collection_ref.document(store_id) # create subcollection for each store

        store_ref.set({'last_scraped': date.isoformat()}, merge=True)

        coupons_ref = store_ref.collection('coupons') # create subcollection for coupons
        
        
        for coupon in coupons:
            document_ref = coupons_ref.document() # create document reference
            coupon_batch.set(document_ref, coupon)

        coupon_batch.commit()
        print(f'Added {len(coupons)} coupons to {chain_name}: {store_id} collection for {date}.')

    except Exception as e:
        print(f'Error adding document to {collection_ref}: {e}.')



def checkStoreScrapedToday(chain_name: str, store_id: str):
    # check if store has already been scraped on current calendar day
    store_ref = db.collection(chain_name).document(store_id)
    storeData = store_ref.get().to_dict() # retrieve store data as an accessible dictionary

    if storeData:
        last_scraped = storeData.get('last_scraped')

        if last_scraped:
            last_scraped_date = datetime.fromisoformat(last_scraped).date()

            if last_scraped_date == date:
                print (f'Data from {chain_name}: {store_id} has already been collected today -- {date}.')
                return True
            
    return False
            


def deleteCoupons(chain_name: str, store_id: str):
    
    try: 

        store_ref = db.collection(chain_name).document(store_id)
        coupons_ref = store_ref.collection('coupons')

        coupons = list(coupons_ref.stream()) # retrieve all coupon documents

        if coupons: 

            dateScraped = store_ref.get().to_dict().get('last_scraped')
            store_ref.set({'last_scraped': None}, merge=True)

            toDelete_batch = db.batch()

            for coupon in coupons:
                toDelete_batch.delete(coupons_ref.document(coupon.id))

            print(f'Deleted all coupons for {chain_name}: {store_id} from {dateScraped}.')

    except Exception as e:
        print(f'Error deleting coupons for {chain_name}: {store_id} -- {e}.')



def pullFromDB(chain_name: str, store_id: str):

    coupons_ref = db.collection(chain_name).document(store_id).collection('coupons')

    coupons = coupons_ref.get()

    if coupons.exists:
        return coupons.to_dict()
    else:
        return print('Error: data does not exist.')

