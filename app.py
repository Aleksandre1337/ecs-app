from flask import Flask, jsonify, request, redirect, url_for, render_template
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB configuration
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
MONGO_DB = os.getenv('MONGO_DB', 'ecs_demo')


def get_mongo_client():
    try:
        client = MongoClient(
            host=MONGO_HOST,
            port=MONGO_PORT,
            serverSelectionTimeoutMS=2000
        )
        client.admin.command('ping')
        return client
    except ConnectionFailure:
        return None


@app.route('/health')
def health():
    client = get_mongo_client()
    status = "connected" if client else "disconnected"
    if client:
        client.close()
    return jsonify({"status": "healthy", "mongodb": status})

# -------------------- UI --------------------


@app.route('/')
def index():
    client = get_mongo_client()
    db_connected = client is not None

    if not client:
        return render_template('index.html', items=[], db_connected=False), 503

    db = client[MONGO_DB]
    items = list(db.items.find())
    client.close()

    return render_template(
        'index.html',
        items=items,
        db_connected=db_connected)

# -------------------- CRUD --------------------


@app.route('/add', methods=['POST'])
def add_item():
    client = get_mongo_client()
    if not client:
        return "Database connection failed", 503

    data = {
        "name": request.form.get("name"),
        "price": int(request.form.get("price"))
    }

    # Add dynamic fields
    field_keys = request.form.getlist("field_key[]")
    field_values = request.form.getlist("field_value[]")

    for key, value in zip(field_keys, field_values):
        if key.strip():  # Only add if key is not empty
            data[key.strip()] = value

    db = client[MONGO_DB]
    db.items.insert_one(data)
    client.close()

    return redirect(url_for('index'))


@app.route('/delete/<item_id>', methods=['POST'])
def delete_item(item_id):
    client = get_mongo_client()
    if not client:
        return "Database connection failed", 503

    db = client[MONGO_DB]
    db.items.delete_one({"_id": ObjectId(item_id)})
    client.close()

    return redirect(url_for('index'))

# -------------------- API --------------------


@app.route('/api/items', methods=['GET'])
def get_items():
    client = get_mongo_client()
    if not client:
        return jsonify({"error": "Database connection failed"}), 503

    db = client[MONGO_DB]
    items = list(db.items.find({}, {"_id": 0}))
    client.close()

    return jsonify({"items": items, "count": len(items)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
