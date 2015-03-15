from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def getRestaurants():
	return session.query(Restaurant).all()

def getRestaurant(restaurant_id):
	return session.query(Restaurant).filter_by(id = restaurant_id).one()

def getMenuItems(restaurantid):
	return session.query(MenuItem).filter_by(restaurant_id = restaurantid).all()

def getMenuItem(menu_id):
	return session.query(MenuItem).filter_by(id = menu_id).one()

def addRestaurant(restaurant_name):
	restaurant = Restaurant(name = restaurant_name)
	session.add(restaurant)
	session.commit()

def addMenuItem(menuItem_name, menuItem_description, menuItem_price, menuItem_course, menuItem_restaurant_id):
	menuItem = MenuItem(name = menuItem_name, description = menuItem_description, price = menuItem_price, course = menuItem_course, restaurant_id = menuItem_restaurant_id)
	session.add(menuItem)
	session.commit()

def updateRestaurant(restaurant):
	session.add(restaurant)
	session.commit()

def updateMenuItem(menuItem):
	session.add(menuItem)
	session.commit()

def deleteRestaurant(restaurant):
	session.delete(restaurant)
	session.commit()

def deleteMenuItem(menuItem):
	session.delete(menuItem)
	session.commit()

