import os, openai
from openai import OpenAI

from firestore_client import pullFromDB, checkEmbedded, storeEmbeddingInDB

openai.api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI()

def generateEmbeddings(local_stores: dict, allCoupons: dict):
    
    allEmbeddings = {}

    for chain_name, coupons in allCoupons.items():
        
        # avoid unneccessary paid api calls and processing
        wasEmbedded = checkEmbedded(chain_name=chain_name, store_id=local_stores[chain_name])  

        if not wasEmbedded:

            # create list of tuples to couple descriptions with their codes 
            descriptions = [ (coupon['code'], coupon['description'])  for coupon in coupons ]

            # separate list of just the description texts for api call
            descriptionTexts = [ description[1]  for description in descriptions ]

        
            try:
                # api call to openai embedding model
                response = client.embeddings.create(
                    model = 'text-embedding-3-small', 
                    input = descriptionTexts
                )

                embeddings = []  # will be a list of objects in the format [ { embedding: ... ,  code: 1234 } , { ... } , { ... } ]

                # pair each embedding with corresponding coupon code
                for i in range(len(response.data)):
                    embedding = {
                        'code': descriptions[i][0],
                        'embedding': response.data[i].embedding                    
                    }

                    embeddings.append(embedding)


                allEmbeddings[chain_name] = {
                    'store_id': local_stores[chain_name],
                    'embeddings': embeddings 
                }

            except Exception as e:
                print(f'Error generating embeddings for {chain_name}: {e}')

        else: 
            print(f'Embedding previously stored for {chain_name}: {local_stores[chain_name]}.')


    return allEmbeddings

    

"""

structure of allEmbeddings dictionary:

{
    'chain_name': {
        'store_id': '12345',  
        'embeddings': [
            {
                'code': '4321',
                'embedding': [ ..... ]
            },
            {   
                # one dict per coupon
            }
        ]
    },
    # additional dictionaries in same format for all applicable chains
}

"""




local_stores = {
      'Dominos': '10481',
      'PapaJohns': '12897'
}
allCoupons = {}

for key, value in local_stores.items():
    coupons = pullFromDB(chain_name=key, store_id=value)
    allCoupons[key] = coupons


allEmbeddings = generateEmbeddings(local_stores, allCoupons)

if allEmbeddings:
    storeEmbeddingInDB(allEmbeddings)