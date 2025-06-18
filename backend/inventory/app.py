from flask import Flask, jsonify
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client()

INVENTORY_COLLECTION = "inventory"

@app.route('/inventory', methods=['GET'])
def get_inventory():
    docs = db.collection(INVENTORY_COLLECTION).stream()
    inventory = []
    for doc in docs:
        data = doc.to_dict()
        inventory.append({
            "product_id": data.get("product_id"),
            "stock": data.get("stock")
        })
    return jsonify(inventory)

@app.route('/')
def root():
    return "Inventory Service Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
