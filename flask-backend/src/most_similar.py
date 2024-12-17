import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from embedding import userEmbedding


def mostSimilar(userInput: str, allCouponsEmbedded: dict): 

    # use cosine similarity to compare user input embedding to all coupon embeddings #

    user_embedding = np.array(userEmbedding(userInput))

    most_similar_coupon = {}
    highest_similarity = -1 
    
    for chain_name, data in allCouponsEmbedded.items():

        print(f'comparing {chain_name}')
        
        for coupon in data['embeddings']:

            coupon_embedding = np.array(coupon['embedding'])

            similarity = cosine_similarity([user_embedding], [coupon_embedding])[0][0]

            if similarity > highest_similarity:
                highest_similarity = similarity

                most_similar_coupon = {
                    'chain': chain_name,
                    'store_id': data['store_id'],
                    'code': coupon['code'],
                    'price': coupon['price'],
                    'description': coupon['description'],
                    'similarity': highest_similarity
                }

    return most_similar_coupon

