"""
Learning about ORM (Object Relational Mapper) in Python
1. Configuration
2. Class
3. Table
4. Mapper
"""

# =========== CONFIGURATION CODE ===============
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

# =============== CLASS CODE ==================
class Restaurant(Base):
    __tablename__ = 'restaurant'
    pass

class MenuItem(Base):
    __tablename__ = 'menu_item'
    pass


### INSERT THE LINE BELOW AT THE END OF THE FILE ###
engine = create_engine('sqlite:///restaurantmenu.db')
