from database.connection import connect_to_database
from bson import ObjectId

def get_products(): 
    db = connect_to_database();
    products = db.get_collection("products").aggregate([
        {"$match": {"visible": True}},
        {
            "$lookup": {
                "from": "variants",
                "localField": "_id",
                "foreignField": "productID",
                "as": "variants"
            }
        },
        {
            "$match": {
                "variants.quantity": { "$gt": 0 },
            }
        },
        {
            "$project": {
                "_id": 1,
                "name": 1
            }
        }
    ])
    return list(products)

def get_products_with_order_and_cart(user_id):
    db = connect_to_database();

    new_user_id = ObjectId(user_id)

    # Truy vấn để lấy ID sản phẩm trong lịch sử mua hàng của người dùng
    products_with_order = db.get_collection("orders").aggregate([
        {"$match": {"userID": new_user_id}},
        {"$lookup": {
            "from": "orderdetails",
            "let": {"orderID": "$_id"},
            "pipeline": [
                {"$match": {"$expr": {"$eq": ["$orderID", "$$orderID"]}}},
                {"$lookup": {
                    "from": "variants",
                    "let": {"variantID": "$variantID"},
                    "pipeline": [
                        {"$match": {"$expr": {"$eq": ["$_id", "$$variantID"]}}}
                    ],
                    "as": "variants"
                }},
                {"$unwind": "$variants"}
            ],
            "as": "details"
        }},
        {"$unwind": "$details"},
        {"$group": {"_id": "$details.variants.productID"}}
    ])

    # Truy vấn để lấy ID sản phẩm trong giỏ hàng của người dùng
    products_with_cart = db.get_collection("carts").aggregate([
        {"$match": {"userID": new_user_id}},
        {"$lookup": {
            "from": "cartdetails",
            "let": {"cartID": "$_id"},
            "pipeline": [
                {"$match": {"$expr": {"$eq": ["$cartID", "$$cartID"]}}},
                {"$lookup": {
                    "from": "variants",
                    "let": {"variantID": "$variantID"},
                    "pipeline": [
                        {"$match": {"$expr": {"$eq": ["$_id", "$$variantID"]}}}
                    ],
                    "as": "variants"
                }},
                {"$unwind": "$variants"}
            ],
            "as": "details"
        }},
        {"$unwind": "$details"},
        {"$group": {"_id": "$details.variants.productID"}}
    ])

    products = set()
    for product in products_with_order:
        if product["_id"]:
            products.add(str(product["_id"]))

    for product in products_with_cart:
        if product["_id"]:
            products.add(str(product["_id"]))

    return list(products)