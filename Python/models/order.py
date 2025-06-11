class Order:
    _id_counter = 1

    def __init__(self, customer_name, meal_quantities):
        self.id = Order._id_counter
        Order._id_counter += 1
        self.customer_name = customer_name
        self.meal_quantities = meal_quantities  # dict of meal_name: quantity

orders = []
