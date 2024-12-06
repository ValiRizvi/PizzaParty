import os 
from google.cloud import firestore

firebase_credentials = os.getenv("FIREBASE_ADMIN_CREDENTIALS")

db = firestore.Client.from_service_account_json(firebase_credentials)


def testFirestore():
    collections = db.collections()
    collectionNames = [collection.id for collection in collections]

    if collectionNames:
        print(f"collections: {collectionNames}")
    else:
        print("no collections stored.")

testFirestore()