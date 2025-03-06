from flask import jsonify, request
from recommender.similar_product import get_recommendation_products
from recommender.recommendation_product import get_recommendation_products as get_recommendations

def routes(app):
    @app.route("/api/recommendations/similar-products/<product_id>", methods=["GET"])
    def get_similar_products_api(product_id):
        limit = request.args.get("limit", 10, type=int)
        print("limit", limit)

        res = get_recommendation_products(product_id, limit)
        return jsonify(res)
    
    @app.route("/api/recommendations/recommendation-products/<user_id>", methods=["GET"])
    def get_recommendation_products_api(user_id):
        limit = request.args.get("limit", 10, type=int)
        print("limit", limit)

        res = get_recommendations(user_id, limit)
        return jsonify(res)