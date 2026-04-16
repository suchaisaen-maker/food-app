from flask import Flask, render_template, request, redirect
from models import db, Food

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    foods = Food.query.all()
    return render_template('index.html', foods=foods)

@app.route('/add', methods=['POST'])
def add_food():
    name = request.form['name']
    category = request.form['category']
    price = request.form['price']
    image = request.form['image']
    new_food = Food(name=name, category=category, price=float(price), image=image)
    db.session.add(new_food)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_food(id):
    food = Food.query.get_or_404(id)
    if request.method == 'POST':
        food.name = request.form['name']
        food.category = request.form['category']
        food.price = float(request.form['price'])
        food.image = request.form['image']
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', food=food)

@app.route('/delete/<int:id>')
def delete_food(id):
    food = Food.query.get_or_404(id)
    db.session.delete(food)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
