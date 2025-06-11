from flask import Flask, render_template
from controllers.meal_controller import meal_bp
from controllers.order_controller import order_bp

app = Flask(__name__, template_folder="views/templates")
app.register_blueprint(meal_bp)
app.register_blueprint(order_bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
