from flask import Blueprint, request, redirect, render_template
from models.meal import Meal, meals

meal_bp = Blueprint("meal_bp", __name__)

@meal_bp.route("/meals/add", methods=["GET", "POST"])
def add_meal():
    if request.method == "POST":
        name = request.form["name"].strip()
        price = request.form["price"].strip()
        try:
            price = float(price)
        except ValueError:
            price = 0.0

        if name and price > 0:
            meals.append(Meal(name, price))
            return redirect("/")
    return render_template("add_meal.html")
