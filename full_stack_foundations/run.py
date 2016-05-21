from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from full_stack_foundations.database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

if __name__ == '__main__':
    items = session.query(MenuItem)
    for item in items:
        # print(item.name)
        pass
    # print(restaurant.all())
    # print(items.all())
    # print(repr(session.query(MenuItem).filter_by(name='Veggie Burgers')))
    # veggie_burgers = session.query(MenuItem).filter_by(name='Veggie Burger')
    iced_tea = session.query(MenuItem).filter_by(id=8).one()
    print(iced_tea)
    print(iced_tea.name)
    print(iced_tea.price)
    iced_tea.price = '$2.99'
    session.add(iced_tea)
    print(session.query(MenuItem).filter_by(id=8).one().price)
    # for burger in veggie_burgers:
    # print(burger.id)
    # print(burger.price)
    # print(burger.restaurant.name)
    # print('=====================\n')
    # session.query(Restaurant).delete()
    # session.commit()
