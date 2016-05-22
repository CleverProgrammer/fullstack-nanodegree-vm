from flask import Flask, Response
from database_setup import Restaurant, Base, MenuItem
from run import session
# from .run import session
app = Flask(__name__)

@app.route('/')
@app.route('/hello')
def hello_world():
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    # items = session.query(MenuItem).all()
    return Response(''.join((item.name+'</br>'+item.price+'</br>'+item.description+'<br><br>' for item in items)))

@app.route('/restaurants/<int:restaurant_id>/')
def display_restaurants(restaurant_id):
    # restaurants = session.query(Restaurant).all()
    restaurant = session.query(Restaurant).get(restaurant_id)
    # return Response(''.join((restarant.name+'<br><br>' for restaurant in restaurants)))
    return Response(restaurant.name)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)