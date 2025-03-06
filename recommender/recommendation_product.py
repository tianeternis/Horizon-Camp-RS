import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from database.product import get_products, get_products_with_order_and_cart

def get_recommendations(products, user_products, limit):
    products= [{"_id": str(product["_id"]), "name": product["name"]} for product in products]
    df_products = pd.DataFrame(products)

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df_products["name"].values)

    similarity = cosine_similarity(tfidf_matrix)

    products_index = [index for index, product_id in enumerate(df_products["_id"]) if product_id in user_products]

    mean_similarity = []

    # for index, similarity_item in list(enumerate(similarity)):
    #     if index not in products_index:
    #         similarity_item = list(enumerate(similarity_item))
    #         total_similarity = 0
    #         for i in products_index:
    #             total_similarity += similarity_item[i][1]
    #         mean_similarity.append((index, total_similarity / len(products_index)))

    similarity = np.array(similarity)
    for index in range(len(similarity)):
        if index not in products_index:
            total_similarity = np.mean(similarity[index, products_index])
            mean_similarity.append((index, total_similarity))

    sorted_mean_similarity = sorted(mean_similarity, key=lambda x:x[1], reverse=True)
    top_similarity_products = sorted_mean_similarity[:limit]

    recommendations = [str(products[value[0]]["_id"]) for value in top_similarity_products]

    return recommendations

def get_recommendation_products(user_id, limit):
    user_products = get_products_with_order_and_cart(user_id)

    if (user_products):
        products = get_products()
        return get_recommendations(products, user_products, limit)
    else:
        return []