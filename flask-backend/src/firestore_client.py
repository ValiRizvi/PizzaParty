import os 
from google.cloud import firestore

firebase_credentials = os.getenv("FIREBASE_ADMIN_CREDENTIALS")

db = firestore.Client.from_service_account_json(firebase_credentials)


def addCouponsToDB(chain_name: str, coupons: dict):

    try:
        coupon_batch = db.batch() # batch coupon writes together for efficiency
        collection_ref = db.collection(chain_name) # create collection for each chain
        
        for coupon in coupons:
            document_ref = collection_ref.document() # create document reference
            coupon_batch.set(document_ref, coupon)

        coupon_batch.commit()
        print(f'Added {len(coupons)} coupons to {chain_name} collection.')

    except Exception as e:
        print(f'Error adding document to {collection_ref}: {e}.')

    
