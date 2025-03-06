from flask import Flask
from api.routes import routes

def main():
    app = Flask(__name__)
    routes(app)
    app.run(debug=True, port=9090)


if __name__ == "__main__":
    main()