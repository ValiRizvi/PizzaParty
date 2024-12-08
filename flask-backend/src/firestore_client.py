import os 
from google.cloud import firestore

firebase_credentials = os.getenv("FIREBASE_ADMIN_CREDENTIALS")

db = firestore.Client.from_service_account_json(firebase_credentials)


def addCouponToDB(chain_name: str, coupons: dict):

    try:
        collection_ref = db.collection(chain_name)
        
        for coupon in coupons:
            collection_ref.add(coupon)
            print(f'document added to {collection_ref}')

    except Exception as e:
        print(f'error adding document to {collection_ref}: {e}')

    
