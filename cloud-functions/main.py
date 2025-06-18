import base64
import json
from google.cloud import pubsub_v1
from google.cloud import firestore

publisher = pubsub_v1.PublisherClient()
INVENTORY_TOPIC = "projects/retail-1234/topics/inventory-updates"
db = firestore.Client()
INVENTORY_COLLECTION = "inventory"

def process_sales(event, context):
    """Triggered from a message on 'sales-events' topic."""
    if 'data' not in event:
        print("No data found in event")
        return

    try:
        data_str = base64.b64decode(event['data']).decode('utf-8')
        sale = json.loads(data_str)

        product_id = sale.get('product_id')
        quantity_sold = sale.get('quantity')

        if not product_id or not isinstance(quantity_sold, int) or quantity_sold <= 0:
            print(f"Invalid sale data: {sale}")
            return

        # 1. Update Firestore inventory atomically
        doc_ref = db.collection(INVENTORY_COLLECTION).document(str(product_id))

        def transaction_update(transaction, doc_ref):
            snapshot = doc_ref.get(transaction=transaction)
            if snapshot.exists:
                current_stock = snapshot.get('stock') or 0
                new_stock = max(current_stock - quantity_sold, 0)
                transaction.update(doc_ref, {'stock': new_stock})
                print(f"Updated stock from {current_stock} to {new_stock} for product {product_id}")
            else:
                transaction.set(doc_ref, {'stock': 0})
                print(f"Created inventory doc for product {product_id} with stock 0")

        transaction = db.transaction()
        transaction.run(transaction_update, doc_ref)

        # 2. Publish update message to inventory-updates topic
        message_json = json.dumps({
            "product_id": product_id,
            "quantity_sold": quantity_sold
        })
        future = publisher.publish(INVENTORY_TOPIC, message_json.encode('utf-8'))
        future.result()  # Wait for publish to complete

        print(f"Published inventory update for product {product_id}")

    except Exception as e:
        print(f"Error processing sales event: {e}")
