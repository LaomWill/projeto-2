from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

ORDERS = [
    {"id": 101, "user_id": 1, "product": "Notebook Dell", "amount": 3500.00, "status": "delivered", "date": "2024-11-15"},
    {"id": 102, "user_id": 2, "product": "Mouse Logitech", "amount": 150.00, "status": "shipped", "date": "2024-11-20"},
    {"id": 103, "user_id": 1, "product": "Teclado Mecânico", "amount": 450.00, "status": "processing", "date": "2024-11-25"},
    {"id": 104, "user_id": 4, "product": "Monitor LG 27\"", "amount": 1200.00, "status": "delivered", "date": "2024-11-18"},
    {"id": 105, "user_id": 5, "product": "Webcam HD", "amount": 300.00, "status": "shipped", "date": "2024-11-28"},
    {"id": 106, "user_id": 2, "product": "Headset Gamer", "amount": 400.00, "status": "processing", "date": "2024-11-29"}
]

@app.route('/')
def home():
    return jsonify({
        "service": "Order Service",
        "version": "2.0.0",
        "description": "Microsserviço de gerenciamento de pedidos",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/orders', methods=['GET'])
def get_orders():
    print(f"[ORDER-SERVICE] GET /orders - Retornando {len(ORDERS)} pedidos")
    return jsonify({
        "service": "Order Service",
        "total": len(ORDERS),
        "orders": ORDERS,
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = next((o for o in ORDERS if o['id'] == order_id), None)
    if order:
        print(f"[ORDER-SERVICE] GET /orders/{order_id} - Pedido: {order['product']}")
        return jsonify({"service": "Order Service", "order": order}), 200
    else:
        print(f"[ORDER-SERVICE] GET /orders/{order_id} - Não encontrado")
        return jsonify({"error": "Pedido não encontrado"}), 404

@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    user_orders = [o for o in ORDERS if o['user_id'] == user_id]
    print(f"[ORDER-SERVICE] GET /orders/user/{user_id} - {len(user_orders)} pedidos encontrados")
    return jsonify({
        "service": "Order Service",
        "user_id": user_id,
        "total": len(user_orders),
        "orders": user_orders,
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "service": "Order Service",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    print("Order Service iniciando na porta 5002...")
    app.run(host='0.0.0.0', port=5002, debug=False)
