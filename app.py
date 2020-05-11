from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
stores = []


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/stores/<string:name>", methods=['GET'])
def get_store(name):
    store = get_store_by_name(name)
    if store:
        return jsonify({"store": store})

    return jsonify({'message': 'store not found'}, 204)


@app.route("/stores", methods=['GET'])
def get_stores():
    return jsonify({"stores": stores}, 200)


@app.route("/stores/<string:name>/items", methods=['GET'])
def get_items_in_store(name):
    store = get_store_by_name(name)
    if store:
        return jsonify({'items': store.get('items')}, 200)

    return jsonify({'message': 'store not found'}, 204)


@app.route("/stores", methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': request_data.get('items', [])
    }

    stores.append(new_store)
    return jsonify(new_store, 201)


@app.route("/stores/<string:name>/items", methods=['POST'])
def create_item_in_store(name):
    store = get_store_by_name(name)
    request_data = request.get_json()

    if store:
        new_item = {
            'name': request_data.get('name'),
            'price': request_data.get('price', 0.0)
        }

        store['items'].append(new_item)
        return jsonify(new_item)

    return jsonify({'message': 'store not found'}, 204)


def get_store_by_name(name):
    for store in stores:
        if store.get('name') == name:
            return store

    return None


if __name__ == '__main__':
    app.run(port=5000, debug=True)
