import base64
import json
from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client()
TABLE_ID = "retail-1234.analytics.sales_events"  # <-- update if project/dataset name is different

def log_sales(event, context):
    if 'data' in event:
        data_str = base64.b64decode(event['data']).decode('utf-8')
        sale = json.loads(data_str)

        row = {
            "product_id": str(sale.get("product_id")),
            "quantity": int(sale.get("quantity")),
            "timestamp": datetime.utcnow().isoformat()
        }

        errors = client.insert_rows_json(TABLE_ID, [row])
        if errors:
            print("BigQuery insert errors:", errors)
        else:
            print("Inserted row into BigQuery:", row)
