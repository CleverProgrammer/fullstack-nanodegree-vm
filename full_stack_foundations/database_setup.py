"""
Learning about ORM (Object Relational Mapper) in Python
1. Configuration
2. Class
3. Table
4. Mapper
"""

# =========== CONFIGURATION ===============
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# =============== CLASSES ==================
class Restaurant(Base):
    """
    Restaurant table using an ORM.
    """
    __tablename__ = 'restaurant'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)


class MenuItem(Base):
    """
    MenuItem table using an ORM.
    """
    __tablename__ = 'menu_item'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    def __repr__(self):
        return "<User(name='%s', id='%s', price='%s')>" % (
            self.name, self.id, self.price)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'name'       : self.name,
            'description': self.description,
            'id'         : self.id,
            'price'      : self.price,
            'course'     : self.course,
        }


### INSERT THE LINE BELOW AT THE END OF THE FILE ###
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
