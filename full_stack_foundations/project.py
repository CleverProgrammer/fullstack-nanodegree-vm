from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Make an API Endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(MenuItems=[item.serialize for item in items])


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', items=items, restaurant=restaurant)


# Task 1: Create route for new_menu_item function here
@app.route('/restaurant/<int:restaurant_id>/new', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
    if request.method == 'POST':
        new_item = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(new_item)
        session.commit()
        flash('Successfully added %s to the menu!' % new_item.name, category='messages')
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant.id))
    return render_template('new_menu_item.html', restaurant=restaurant)


# Task 2: Create route for edit_menu_item function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
    menu = session.query(MenuItem).filter(MenuItem.id == menu_id).one()
    if request.method == 'POST':
        menu.name = request.form['name']
        session.commit()
        flash('Successfully edited %s in menu!' % menu.name, category='messages')
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    return render_template('edit_menu_item.html', restaurant=restaurant, menu=menu)


# Task 3: Create a route for delete_menu_item function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
    menu = session.query(MenuItem).filter(MenuItem.id == menu_id).one()
    if request.method == 'POST':
        delete_item_name = menu.name
        session.query(MenuItem).filter(MenuItem.id == menu_id).delete()
        session.commit()
        flash('Successfully deleted %s from the menu!' % delete_item_name, category='messages')
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    return render_template('delete_menu_item.html', restaurant=restaurant, menu=menu)


if __name__ == '__main__':
    app.secret_key = 'Billy'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
