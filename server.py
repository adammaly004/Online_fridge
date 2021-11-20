from flask import Flask, flash, request, redirect, render_template, url_for
from utils import *

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


FRIDGE = open_file('data/fridge.json')
RECIPES = open_file('data/resource.json')


c = Cook(RECIPES, FRIDGE)


@ app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        text = request.form['text'].lower()
        num = request.form['num']

        updated_fridge = c.add_item(text, num)
        open_file('data/fridge.json', "w", updated_fridge)

    FRIDGE = open_file('data/fridge.json')
    name = c.check_resource()
    return render_template("index.html", fridge=FRIDGE.items(), food=name)


@ app.route('/info/<food>', methods=['GET', 'POST'])
def info(food):
    recipe = c.show_info(food)
    return render_template("info.html", info=recipe, food=food)


@ app.route('/update/<food>', methods=['GET', 'POST'])
def find(food):
    FRIDGE = c.update_fridge(food)
    open_file('data/fridge.json', "w", FRIDGE)
    return redirect("/")


@ app.route('/all', methods=['GET', 'POST'])
def all():
    return render_template('all.html', recipes=RECIPES)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=1111)
