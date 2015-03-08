from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

session = DBSession()

myRestaurant = Restaurant(name = "Pizza Palace")
session.add(myRestaurant)
session.commit()

#session.query(Restaurant).all()

cheesePizza = MenuItem(name = "Cheese Pizza", description = "Made with natual ingredients and cheese",
	course = "Entree", price = "R10.99", restaurant = myRestaurant)
session.add(cheesePizza)
session.commit()