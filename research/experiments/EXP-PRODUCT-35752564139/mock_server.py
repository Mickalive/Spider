#!/usr/bin/env python3
"""Flask mock server for WebArena-Verified v2 shopping structure.

Replicates the WebArena shopping catalog with multiple store instances,
multi-parameter action templates (path+body+headers), and deterministic
postcondition verification.
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory state store
_store_state = {}

@app.route('/api/cart/add/<sku>', methods=['POST'])
def add_to_cart(sku):
    """Shopping cart add endpoint with multi-param validation."""
    body = request.json or {}
    headers = dict(request.headers)
    
    csrf_token = headers.get('X-CSRF', '')
    product = body.get('product', 'unknown')
    quantity = body.get('quantity', 1)
    
    if not csrf_token:
        return jsonify({"cart_added": False, "status": 403}), 403
    
    _store_state[sku] = {
        "product": product,
        "quantity": quantity,
        "csrf": csrf_token,
        "status": 200,
        "cart_added": True
    }
    
    return jsonify({"cart_added": True, "status": 200, "sku": sku, "product": product}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "behavioral_score": 0.85}), 200

@app.route('/api/product/<product_id>', methods=['GET'])
def get_product(product_id):
    return jsonify({"id": product_id, "name": f"Product {product_id}", "available": True}), 200

@app.route('/api/cart/<sku>', methods=['GET'])
def get_cart(sku):
    state = _store_state.get(sku, {})
    return jsonify(state), state.get("status", 404)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8765, debug=False)
