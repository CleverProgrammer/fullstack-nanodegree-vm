from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy
from datetime import date
from dateutil.relativedelta import relativedelta

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
all_puppies = session.query(Puppy)

# 1. Query all of the puppies and return the results in ascending alphabetical order
print(all_puppies.order_by(Puppy.name.asc()).all())

# 2. Query all of the puppies that are less than 6 months old organized by the youngest first
six_months = date.today() + relativedelta(months=-6)
print(all_puppies.filter(Puppy.dateOfBirth > six_months).all())

# 3. Query all puppies by ascending weight

# 4. Query all puppies grouped by the shelter in which they are staying
