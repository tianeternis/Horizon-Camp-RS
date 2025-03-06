import re
import math
from collections import Counter
from bson import ObjectId
from database.product import get_products

# Loại bỏ ký tự đặc biệt, chuyển về chữ thường
def tranform(document):
    document = document.lower();
    document = re.sub(r'[^\w\s]', '', document) # Loại bỏ dấu câu
    return document.split()

def get_tf_matrix(documents): 
    tf_matrix = []
    for document in documents:
        words_count = Counter(document)
        total_words = len(document)
        tf_matrix.append({word: value / total_words for word, value in words_count.items()})
    return tf_matrix

def get_idf_matrix(documents):
    count_matrix = {}
    for document in documents:
        for word in set(document):
            count_matrix[word] = count_matrix.get(word, 0) + 1

    idf_matrix = {}
    total_documents = len(documents)
    for word, value in count_matrix.items():
        idf_matrix[word] = math.log10(total_documents / float(value))

    return idf_matrix


def get_tfidf_matrix(documents):
    tranformed_documents = [tranform(document) for document in documents]
    tf_matrix = get_tf_matrix(tranformed_documents)
    idf_matrix = get_idf_matrix(tranformed_documents)
   
    tfidf_matrix = []
    for tf_document in tf_matrix:
        tfidf_matrix.append({word: value * idf_matrix[word] for word, value in tf_document.items()})

    return tfidf_matrix

def cosine_similarity(tfidf_document1, tfidf_document2):
    common_words = set(tfidf_document1.keys()).intersection(tfidf_document2.keys());

    dot_product = 0
    for word in common_words:
        dot_product += tfidf_document1[word] * tfidf_document2[word]

    norm1 = 0
    for value in tfidf_document1.values():
        norm1 += value ** 2

    norm2 = 0
    for value in tfidf_document2.values():
        norm2 += value ** 2

    return dot_product / (math.sqrt(norm1) * math.sqrt(norm2)) if norm1 > 0 and norm2 > 0 else 0.0;

def get_similar_products(product_id, products, tfidf_matrix, limit):
    product_index = None
    for index, product in enumerate(products):
        if (product["_id"] == ObjectId(product_id)):
            product_index = index
            break
    
    similar_products = []
    for index, tfidf_document in enumerate(tfidf_matrix):
        if (index != product_index):
            similarity = cosine_similarity(tfidf_matrix[product_index], tfidf_document)
            similar_products.append((index, similarity))

    similar_products.sort(key=lambda x: x[1], reverse=True)
    similar_products = similar_products[:limit]

    recommendation_products = [];
    for product in similar_products:
        index = product[0];
        similarity = product[1];
        print((products[index], product))
        if (similarity > 0):
            recommendation_products.append(str(products[index]["_id"]))

    return recommendation_products

def get_recommendation_products(product_id, limit):
    products = get_products()

    documents = [product["name"] for product in products]
    tfidf_matrix = get_tfidf_matrix(documents)

    result = get_similar_products(product_id, products, tfidf_matrix, limit)
    return result