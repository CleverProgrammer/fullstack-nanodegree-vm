#!/Users/Rafeh/anaconda/bin python
"""
Puppy shelter project!

Author: Rafeh Qazi
Modified: May 2016
"""


# =========== CONFIGURATION CODE ===============
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

# =============== CLASS CODE ==================
class Shelter(Base):
    __tablename__ = 'shelter'
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zipCode = Column(Integer, nullable=False)
    website = Column(String)
    id = Column(Integer, primary_key=True)


class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    dateOfBirth = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)
    picture = Column(String, nullable=False)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)

    def __repr__(self):
        return "<Puppy(name='%s', dateOfBirth='%s', gender='%s')>" % (
            self.name, self.dateOfBirth, self.gender)

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.create_all(engine)
