import os, openai
from openai import OpenAI

from utils.firestore_client import pullFromDB, checkEmbedded, storeEmbeddingInDB

openai.api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI()


# embed the user input
def userEmbedding(userInput: str):

    try:
        response = client.embeddings.create(
            model='text-embedding-3-small',  
            input=userInput
        )
        embedding = response.data[0].embedding 

        return embedding
    
    except Exception as e:
        print(f'Error generating user input embedding: {e}.')


# embed coupons
def generateEmbeddings(local_stores: dict, allCoupons: dict):
    
    allCouponsEmbedded = {}

    embeddedInDB = []

    for chain_name, coupons in allCoupons.items():
        
        # avoid unneccessary paid api calls and processing
        wasEmbedded = checkEmbedded(chain_name=chain_name, store_id=local_stores[chain_name]) 

        print(f'{chain_name}: {local_stores[chain_name]} wasEmbedded = {wasEmbedded}') 
        

        if wasEmbedded:

            embeddedInDB.append(chain_name)

            print(f'Embedding previously stored for {chain_name}: {local_stores[chain_name]}.')
            
            continue  # skip embedding generation for current loop iteration


        # create list of tuples to couple descriptions with their codes 
        descriptions = [ (coupon['code'], coupon['description'], coupon['price'])  for coupon in coupons ]

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
                    'description': descriptions[i][1],
                    'price': descriptions[i][2],
                    'embedding': response.data[i].embedding                    
                }

                embeddings.append(embedding)


            allCouponsEmbedded[chain_name] = {
                'store_id': local_stores[chain_name],
                'embeddings': embeddings 
            }

        except Exception as e:
            print(f'Error generating embeddings for {chain_name}: {e}')


    storeEmbeddingInDB(allCouponsEmbedded) # store newly generated embeddings in DB

    print(embeddedInDB)
    # collect previosuly stored embeddings and add to allCouponsEmbedded
    for chain_name in embeddedInDB:

        allCouponsEmbedded[chain_name] = {
            'store_id': local_stores[chain_name],
            'embeddings': pullFromDB(
                            chain_name=chain_name, 
                            store_id=local_stores[chain_name], 
                            collection_to_pull='embedded_coupons'
                        ) 
        }


    return allCouponsEmbedded

"""

structure of allCouponsEmbedded dictionary:

{
    'chain_name': {
        'store_id': '12345',  
        'embeddings': [
            {
                'code': '4321',
                'description': ' ... ',
                'price': '12.99',
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










   