from flask import Blueprint, request, redirect, render_template, abort
from models.order import Order, orders
from models.meal import meals

order_bp = Blueprint("order_bp", __name__)

@order_bp.route("/orders/add", methods=["GET", "POST"])
def add_order():
    if request.method == "POST":
        customer_name = request.form["customer_name"].strip()
        meal_quantities = {}

        for meal in meals:
            qty_str = request.form.get(f"quantity_{meal.name}", "0")
            try:
                qty = int(qty_str)
            except ValueError:
                qty = 0
            if qty > 0:
                meal_quantities[meal.name] = qty

        if customer_name and meal_quantities:
            orders.append(Order(customer_name, meal_quantities))
            return redirect("/orders")
    return render_template("add_order.html", meals=meals)

@order_bp.route("/orders")
def list_orders():
    return render_template("list_orders.html", orders=orders)

@order_bp.route("/orders/<int:order_id>/edit", methods=["GET", "POST"])
def edit_order(order_id):
    order = next((o for o in orders if o.id == order_id), None)
    if order is None:
        abort(404, "Order not found")

    if request.method == "POST":
        customer_name = request.form["customer_name"].strip()
        meal_quantities = {}

        for meal in meals:
            qty_str = request.form.get(f"quantity_{meal.name}", "0")
            try:
                qty = int(qty_str)
            except ValueError:
                qty = 0
            if qty > 0:
                meal_quantities[meal.name] = qty

        if customer_name and meal_quantities:
            order.customer_name = customer_name
            order.meal_quantities = meal_quantities
            return redirect("/orders")

    return render_template("edit_order.html", order=order, meals=meals)

@order_bp.route("/orders/stats")
def orders_stats():
    total_orders = len(orders)
    total_meals = sum(qty for order in orders for qty in order.meal_quantities.values())
    total_revenue = 0.0

    for order in orders:
        for meal_name, qty in order.meal_quantities.items():
            meal = next((m for m in meals if m.name == meal_name), None)
            if meal:
                total_revenue += meal.price * qty

    return render_template("orders_stats.html",
                           orders=orders,
                           total_orders=total_orders,
                           total_meals=total_meals,
                           total_revenue=total_revenue)
