from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', items=items, restaurant=restaurant)


# Task 1: Create route for new_menu_item function here
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    restaurant = session.query(Restaurant).filter(Restaurant.id==restaurant_id).one()
    if request.method == 'POST':
        new_item = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(new_item)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant.id))
    return render_template('new_menu_item.html', restaurant=restaurant)

# Task 2: Create route for edit_menu_item function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter(Restaurant.id==restaurant_id).one()
    menu = session.query(MenuItem).filter(MenuItem.id==menu_id).one()
    if request.method == 'POST':
        menu.name = request.form['name']
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    return render_template('edit_menu_item.html', restaurant=restaurant, menu=menu)

# Task 3: Create a route for delete_menu_item function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter(Restaurant.id==restaurant_id).one()
    menu = session.query(MenuItem).filter(MenuItem.id==menu_id).one()
    if request.method == 'POST':
        session.query(MenuItem).filter(MenuItem.id==menu_id).delete()
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    return render_template('delete_menu_item.html', restaurant=restaurant, menu=menu)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
