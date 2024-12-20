import os 
from google.cloud import firestore
from datetime import datetime

firebase_credentials = os.getenv("FIREBASE_ADMIN_CREDENTIALS")

db = firestore.Client.from_service_account_json(firebase_credentials)

currentTime = datetime.now()
date = currentTime.date()


##  ALL FIRESTORE INTERACTIVE FUNCTIONS ARE DEFINED IN THIS FILE  ##


def addCouponsToDB(chain_name: str, store_id: str, coupons: list):

    deleteCoupons(chain_name, store_id, 'coupons') # delete outdated coupons if they exist
    deleteCoupons(chain_name, store_id, 'embedded_coupons')

    try:
        coupon_batch = db.batch() # batch coupon writes together for efficiency
        collection_ref = db.collection(chain_name) # create collection for each chain
        store_ref = collection_ref.document(store_id) # create subcollection for each store

        store_ref.set({'last_scraped': date.isoformat()}, merge=True) # set last_scraped property to current date

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
            


def deleteCoupons(chain_name: str, store_id: str, collection_to_delete: str):
    
    try: 

        store_ref = db.collection(chain_name).document(store_id)
        coupons_ref = store_ref.collection(collection_to_delete)

        coupons = list(coupons_ref.stream()) # retrieve all coupon documents

        if coupons: 

            dateScraped = store_ref.get().to_dict().get('last_scraped')
            store_ref.set({'last_scraped': None}, merge=True)
            store_ref.set({'embedded': False}, merge=True)

            toDelete_batch = db.batch()

            for coupon in coupons:
                toDelete_batch.delete(coupon.reference)

            toDelete_batch.commit()

            print(f'Deleted all coupons for {chain_name}: {store_id} in {collection_to_delete} from {dateScraped}.')

    except Exception as e:
        print(f'Error deleting coupons for {chain_name}: {store_id} -- {e}.')



# pulls all coupons for a given store from database

def pullFromDB(chain_name: str, store_id: str, collection_to_pull: str):

    coupons_ref = db.collection(chain_name).document(store_id).collection(collection_to_pull)

    coupons = coupons_ref.get()

    couponCollection = []

    if coupons:
        for coupon in coupons:
            couponCollection.append(coupon.to_dict())
    
    return couponCollection



# function just for pulling a single coupon 

from google.cloud.firestore_v1.base_query import FieldFilter  # need FieldFilter to avoid warning messages (still works without this)

def getCouponFromFirestore(bestCouponInfo: dict):
    
    chain_name = bestCouponInfo['chain']
    store_number = bestCouponInfo['store_id']
    code = bestCouponInfo['code']


    chain_ref = db.collection(chain_name)

    store_ref = chain_ref.document(store_number).collection('coupons')

    coupon_ref = store_ref.where(filter=FieldFilter(field_path='code', op_string='==', value=code))

    results = coupon_ref.get()

    if results:
        coupon = results[0]  # retrieve first match
        bestCouponInfo['coupon'] = coupon.to_dict()

        return bestCouponInfo
    
    else:
        print(f'No coupon with code: {code} in {chain_name}: {store_number}.')
        return None



def checkEmbedded(chain_name: str, store_id: str):

    store_ref = db.collection(chain_name).document(store_id)

    try: 
        embedded = store_ref.get().to_dict().get('embedded')
        return embedded

    except:
        return False



def storeEmbeddingInDB(allCouponsEmbedded: dict):

    try:
        # loop through each chain in dictionary
        for chain_name, store_data in allCouponsEmbedded.items():

            store_id = store_data['store_id']
            embeddings = store_data['embeddings']

            store_ref = db.collection(chain_name).document(store_id)

            # reference for embedding subcollection under current store collection, to be at same level as coupons collection
            embedding_ref = store_ref.collection('embedded_coupons')

            # Iterate over each embedding and store it along with its corresponding coupon code
            for item in embeddings:
                embedding_ref.add({
                    'code': item['code'],
                    'price': item['price'],
                    'description': item['description'],
                    'embedding': item['embedding']
                })

            print(f'Embeddings stored for {chain_name}: {store_id}.')

            # set field to later reference when checking if data was already embedded
            store_ref.set({'embedded': True}, merge=True)
    
    except Exception as e:
        print(f'Error storing embeddings: {e}')





