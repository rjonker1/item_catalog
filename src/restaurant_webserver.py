## Flask micro framework ##
from flask import Flask, render_template, request, redirect, url_for, jsonify, url_for,flash, Markup, abort
from flask_bootstrap import Bootstrap
from jinja2 import TemplateNotFound
app = Flask(__name__)

## Fakes  ##
#import fakes

## DAL ##
import database_access
## Api returning JSON ##

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	try:
		restaurant = database_access.getRestaurant(restaurant_id)
		items = database_access.getMenuItems(restaurant_id)
		return jsonify(MenuItems=[i.serialize for i in items])
	except Exception:
		abort(500)
	

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
	try:
		Menu_Item = database_access.getMenuItem(menu_id)
		return jsonify(Menu_Item = Menu_Item.serialize)
	except Exception:
		abort(500)

@app.route('/restaurants/JSON')
def restaurantsJSON():
	try:
		restaurants = database_access.getRestaurants()
		return jsonify(restaurants= [r.serialize for r in restaurants])
	except Exception:
		abort(500)	

#Show all restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	try:
		restaurants = database_access.getRestaurants()
		return render_template('restaurants.html', restaurants = restaurants)
	except TemplateNotFound:
		abort(404)
	except Exception:
		abort(500)	

#Show a restaurant menu
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	try:
		restaurant = database_access.getRestaurant(restaurant_id)
		items = database_access.getMenuItems(restaurant_id)
		return render_template('menu.html', items = items, restaurant = restaurant)
	except TemplateNotFound:
		abort(404)
	except Exception:
		abort(500)

#Create a new restaurant
@app.route('/restaurants/new', methods=['GET','POST'])
def newRestaurant():
	try:
		if request.method == 'POST':
			name = request.form['name']
			database_access.addRestaurant(name)
			message = Markup("<h4>%s Created</h4>" % name )
			flash(message)
			return redirect(url_for('showRestaurants'))
		else:
			return render_template('newRestaurant.html')		
	except TemplateNotFound:
		abort(404)
	except Exception:
		abort(500)
	

#Create a new menu item
@app.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	try:
		if request.method == 'POST':
			database_access.addMenuItem(request.form['name'], request.form['description'], request.form['price'], request.form['course'], restaurant_id)
			message = Markup("<h4>%s Created</h4>" % request.form['name'])
			flash(message)
			return redirect(url_for('showMenu', restaurant_id = restaurant_id))
		else:
			return render_template('newmenuitem.html', restaurant_id = restaurant_id)		
	except TemplateNotFound:
		abort(404)
	except Exception:
		abort(500)

#Edit a restaurant
@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
	#editedRestaurant = fakes.restaurant	
	try:
		editedRestaurant = database_access.getRestaurant(restaurant_id)
		if request.method == 'POST':
			editedRestaurant.name = request.form['name']
			database_access.updateRestaurant(editedRestaurant)
			message = Markup("<h4>%s Updated</h4>" % editedRestaurant.name)
			flash(message)
			return redirect(url_for('showRestaurants'))
		else:
			return render_template('editRestaurant.html', restaurant = editedRestaurant)
	except TemplateNotFound:
		abort(404)
	except Exception:
		abort(500)	

#Edit a restaurant menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	try:
		editedItem = database_access.getMenuItem(menu_id)
		if request.method == 'POST':
			editedItem.name = request.form['name']
			editedItem.description = request.form['description']
			editedItem.price = request.form['price']
			editedItem.course = request.form['course']
			database_access.updateMenuItem(editedItem)
			message = Markup("<h4>%s Updated</h4>" % editedItem.name)
			flash(message)
			return redirect(url_for('showMenu', restaurant_id = restaurant_id))			
		else:
			return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)
	except TemplateNotFound:
		abort(404)		
	except Exception:
		abort(500)

#Delete a restaurant
@app.route('/restaurants/<int:restaurant_id>/delete', methods = ['GET','POST'])
def deleteRestaurant(restaurant_id):
	try:
		restaurantToDelete = database_access.getRestaurant(restaurant_id)
		if request.method == 'POST':
			database_access.deleteRestaurant(restaurantToDelete)
			message = Markup("<h4>%s Deleted</h4>" % restaurantToDelete.name)
			flash(message)
			return redirect(url_for('showRestaurants', restaurant_id = restaurant_id))
		else:
			return render_template('deleteRestaurant.html',restaurant = restaurantToDelete)
	except TemplateNotFound:
		abort(404)
	except Exception:
		abort(500)

#Delete a menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	try:
		itemToDelete = database_access.getMenuItem(menu_id)
		if request.method == 'POST':
			database_access.deleteMenuItem(itemToDelete)
			message = Markup("<h4>%s Deleted</h4>" % itemToDelete.name)
			flash(message)
			return redirect(url_for('showMenu', restaurant_id = restaurant_id))
		else:
			return render_template('deleteMenuItem.html', item = itemToDelete)
	except TemplateNotFound:
		abort(404)
	except Exception:
		abort(500)		

if __name__ == '__main__':
	app.secret_key = '@123(^0(%'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)