from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'  # SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    plastic = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    plastic_weight = db.Column(db.Float, nullable=False)
    calculated_cost = db.Column(db.Float, nullable=False)
    rounded_cost = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Boolean, nullable=False, default=False)
    net_profit = db.Column(db.Float, nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    orders = Order.query.all()
    return render_template('index.html', orders=orders)

# Create a new order
@app.route('/orders', methods=['POST'])
def create_order():
    model = request.form.get('model')
    plastic = request.form.get('plastic')
    cost = float(request.form.get('cost', 0))
    plastic_weight = float(request.form.get('plastic_weight', 0))
    calculated_cost = float(request.form.get('calculated_cost', 0))
    rounded_cost = float(request.form.get('rounded_cost', 0))
    paid = request.form.get('paid') == 'true'
    net_profit = float(request.form.get('net_profit', 0))

    new_order = Order(
        model=model,
        plastic=plastic,
        cost=cost,
        plastic_weight=plastic_weight,
        calculated_cost=calculated_cost,
        rounded_cost=rounded_cost,
        paid=paid,
        net_profit=net_profit
    )
    db.session.add(new_order)
    db.session.commit()

    return jsonify({"message": "Order created successfully!"}), 201

# Read all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([
        {
            "id": order.id,
            "model": order.model,
            "plastic": order.plastic,
            "cost": order.cost,
            "plastic_weight": order.plastic_weight,
            "calculated_cost": order.calculated_cost,
            "rounded_cost": order.rounded_cost,
            "paid": order.paid,
            "net_profit": order.net_profit
        }
        for order in orders
    ])

# Update an order
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.json
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"message": "Order not found"}), 404

    order.model = data.get('model', order.model)
    order.plastic = data.get('plastic', order.plastic)
    order.cost = data.get('cost', order.cost)
    order.plastic_weight = data.get('plastic_weight', order.plastic_weight)
    order.calculated_cost = data.get('calculated_cost', order.calculated_cost)
    order.rounded_cost = data.get('rounded_cost', order.rounded_cost)
    order.paid = data.get('paid', order.paid)
    order.net_profit = data.get('net_profit', order.net_profit)

    db.session.commit()
    return jsonify({"message": "Order updated successfully!"})

# Delete an order
@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"message": "Order not found"}), 404

    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
