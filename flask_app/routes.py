from flask import Blueprint, jsonify, request, abort
import random
from datetime import datetime

print("ABC")

api_bp = Blueprint('api', __name__)

# Simple in-memory 'database' for demo
DB = {
    'items': [
        {'id': 1, 'name': 'Item One', 'value': 100},
        {'id': 2, 'name': 'Item Two', 'value': 200},
    ]
}

print("abc")


# Helper to find item
def _find_item(item_id):
    for item in DB['items']:
        if item['id'] == item_id:
            return item
    return None

# API 1: health check
@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'time': datetime.utcnow().isoformat() + 'Z'})

# API 2: list items
@api_bp.route('/items', methods=['GET'])
def list_items():
    return jsonify(DB['items'])

# API 3: get item by id
@api_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = _find_item(item_id)
    if not item:
        abort(404)
    return jsonify(item)

# API 4: create item
@api_bp.route('/items', methods=['POST'])
def create_item():
    data = request.get_json() or {}
    if 'name' not in data or 'value' not in data:
        abort(400, 'name and value required')
    new_id = max([i['id'] for i in DB['items']]) + 1 if DB['items'] else 1
    item = {'id': new_id, 'name': data['name'], 'value': data['value']}
    DB['items'].append(item)
    return jsonify(item), 201

# API 5: update item
@api_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = _find_item(item_id)
    if not item:
        abort(404)
    data = request.get_json() or {}
    item.update({k: data[k] for k in ['name', 'value'] if k in data})
    return jsonify(item)

# API 6: delete item
@api_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = _find_item(item_id)
    if not item:
        abort(404)
    DB['items'].remove(item)
    return '', 204

# API 7: random number
@api_bp.route('/random', methods=['GET'])
def random_number():
    return jsonify({'number': random.randint(0, 1000)})

# API 8: echo
@api_bp.route('/echo', methods=['POST'])
def echo():
    data = request.get_json() or {}
    return jsonify({'you_sent': data})

# API 9: stats - simple count and sum
@api_bp.route('/stats', methods=['GET'])
def stats():
    count = len(DB['items'])
    total = sum(i.get('value', 0) for i in DB['items'])
    return jsonify({'count': count, 'total_value': total})

# API 10: uppercase a string
@api_bp.route('/uppercase', methods=['POST'])
def uppercase():
    data = request.get_json() or {}
    s = data.get('text')
    if s is None:
        abort(400, 'text required')
    return jsonify({'upper': str(s).upper()})

# API 11: multiply numbers
@api_bp.route('/multiply', methods=['POST'])
def multiply():
    data = request.get_json() or {}
    a = data.get('a')
    b = data.get('b')
    try:
        a = float(a)
        b = float(b)
    except Exception:
        abort(400, 'a and b must be numbers')
    return jsonify({'result': a * b})
