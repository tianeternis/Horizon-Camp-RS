# Horizon Camp - Recommendation System

Horizon Camp is an e-commerce website selling camping gear, integrating a smart product recommendation system. The recommendation system currently uses Content-based Filtering based on product name, supporting two main functions:
- Suggesting similar products: based on the product being viewed.
- Suggesting products based on user history: based on shopping cart and purchased products.

## 📂 Project Structure

Horizon-Camp-RS/
├── api/                               # Flask routes
│ └── routes.py
├── database/                          # Database connection and model
│ ├── connection.py
│ └── product.py
├── recommender/                       # Recommendation algorithm
│ ├── recommendation_product.py        # Recommendation based on user's shopping history and cart
│ └── similar_product.py               # Suggest similar products
├── main.py                            # Entry point
├── .env                               # Environment variables
└── requirements.txt                   # Required packages

## 💻 Tech Stack

- Backend: Python, Flask, Pandas, Scikit-learn
- Database: MongoDB
- Recommendation: Content-based Filtering (TF-IDF + Cosine Similarity)

## ⚙️ Installation
```bash
git clone https://github.com/tianeternis/Horizon-Camp-RS.git
cd Horizon-Camp-RS
python main.py
```
