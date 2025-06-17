from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Product API is running!"

@app.route('/products', methods=['GET'])
def get_products():
    products = [
        {"product_id": 1, "name": "Laptop", "price": 1200},
        {"product_id": 2, "name": "Mouse", "price": 25}
    ]
    return jsonify(products)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
