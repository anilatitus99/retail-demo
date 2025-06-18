from flask import Flask, jsonify, request
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client()

ORDERS_COLLECTION = "orders"

@app.route('/orders', methods=['GET'])
def get_orders():
    docs = db.collection(ORDERS_COLLECTION).stream()
    orders_list = []

    for doc in docs:
        data = doc.to_dict()
        data['id'] = doc.id
        orders_list.append(data)

    return jsonify(orders_list)

@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    doc = db.collection(ORDERS_COLLECTION).document(order_id).get()
    if doc.exists:
        data = doc.to_dict()
        data['id'] = doc.id
        return jsonify(data)
    else:
        return jsonify({"error": "Order not found"}), 404

@app.route('/orders', methods=['POST'])
def create_order():
    content = request.json
    doc_ref = db.collection(ORDERS_COLLECTION).add(content)
    return jsonify({"status": "order created", "id": doc_ref[1].id}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
