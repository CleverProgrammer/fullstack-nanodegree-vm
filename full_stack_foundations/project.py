from flask import Flask
from database_setup import Restaurant, Base
from run import session
# from .run import session
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/hello')
def hello_world():
    return 'Hello World'

@app.route('/restaurants')
def display_restaurants():
    restaurants = session.query(Restaurant).all()
    print(restaurants)
    output = ''
    for restaurant in restaurants:
        output += restaurant.name + '<br><br>'
    print(output)
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)