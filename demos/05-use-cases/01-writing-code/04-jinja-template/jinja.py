from flask import Flask, render_template
from jinja2 import Template

app = Flask(__name__)

class FoodItem:
    def __init__(self, name, price, calories):
        self.name = name
        self.price = price
        self.calories = calories

@app.route('/')
def home():
    food_item = FoodItem("Pizza", 10.99, 1200)
    return render_template('template.html', name=food_item.name, price=food_item.price, calories=food_item.calories)

if __name__ == '__main__':
    app.run(debug=True)
