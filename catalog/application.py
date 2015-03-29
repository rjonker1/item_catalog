from flask import Flask, render_template, request, session, redirect, url_for, jsonify, url_for,flash, Markup, abort
from jinja2 import TemplateNotFound
from flask.ext.github import GitHub
from rauth.service import OAuth2Service

### Authentication ###
import authentication

## DAL ##
import database_access

app = Flask(__name__)

github = OAuth2Service(
    name='github',
    base_url='https://api.github.com/',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    client_id= '242f572297c24270cd17',
    client_secret= '64527395acf597927c6997eeb90560769e40c303',
)

@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        print(token)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = authentication.getCsrfToken()
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token

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

@app.route('/login')
def login():
	redirect_uri = url_for('authorized', next=request.args.get('next') or 
		request.referrer or None, _external=True)
	print(redirect_uri)
	# More scopes http://developer.github.com/v3/oauth/#scopes
	params = {'redirect_uri': redirect_uri, 'scope': 'user:email'}
	print(github.get_authorize_url(**params))
	return redirect(github.get_authorize_url(**params))

# same path as on application settings page
@app.route('/github-callback')
def authorized():
    # check to make sure the user authorized the request
    if not 'code' in request.args:
        flash('You did not authorize the request')
        return redirect(url_for('showRestaurants'))

    # make a request for the access token credentials using code
    redirect_uri = url_for('authorized', _external=True)

    data = dict(code=request.args['code'],
        redirect_uri=redirect_uri,
        scope='user:email,public_repo')

    auth = github.get_auth_session(data=data)

    # the "me" response
    me = auth.get('user').json()

    session['token'] = auth.access_token

    flash('Logged in as ' + me['name'])
    return redirect(url_for('showRestaurants'))

#Show all restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	try:
		user = authentication.getUser(github)
		if user != None:
			restaurants = database_access.getRestaurants()
			return render_template('restaurants.html', restaurants = restaurants)
		else:
			return redirect(url_for('login'))		
	except TemplateNotFound:
		abort(404)
	except Exception:
		abort(500)

#Show a restaurant menu
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	try:
		user = authentication.getUser(github)
		if user != None:
			restaurant = database_access.getRestaurant(restaurant_id)
			items = database_access.getMenuItems(restaurant_id)
			return render_template('menu.html', items = items, restaurant = restaurant)
		else:
			return redirect(url_for('login'))
	except TemplateNotFound:
		abort(404)
	except Exception:
		abort(500)

#Create a new restaurant
@app.route('/restaurants/new', methods=['GET','POST'])
def newRestaurant():
	#try:
		user = authentication.getUser(github)
		if user != None:
			if request.method == 'POST':
				name = request.form['name']
				database_access.addRestaurant(name)
				message = "%s Created" % name
				flash(message)
				return redirect(url_for('showRestaurants'))
			else:
				return render_template('newRestaurant.html')
		else:
			return redirect(url_for('login'))
	#except TemplateNotFound:
		#abort(404)
	#except Exception:
		#abort(500)
	

#Create a new menu item
@app.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	try:
		user = authentication.getUser(github)
		if user != None:
			if request.method == 'POST':
				database_access.addMenuItem(request.form['name'], request.form['description'], request.form['price'], request.form['course'], restaurant_id)
				message = "%s Created!" % request.form['name']
				flash(message)
				return redirect(url_for('showMenu', restaurant_id = restaurant_id))
			else:
				return render_template('newmenuitem.html', restaurant_id = restaurant_id)
		else:
			return redirect(url_for('login'))
	except TemplateNotFound:
		abort(404)
	except Exception:
		abort(500)

#Edit a restaurant
@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
	#editedRestaurant = fakes.restaurant	
	try:
		user = authentication.getUser(github)
		if user != None:
			editedRestaurant = database_access.getRestaurant(restaurant_id)
			if request.method == 'POST':
				editedRestaurant.name = request.form['name']
				database_access.updateRestaurant(editedRestaurant)
				message = "%s Updated!" % editedRestaurant.name
				flash(message)
				return redirect(url_for('showRestaurants'))
			else:
				return render_template('editRestaurant.html', restaurant = editedRestaurant)
		else:
			return redirect(url_for('login'))
	except TemplateNotFound:
		abort(404)
	except Exception:
		abort(500)	

#Edit a restaurant menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	try:
		user = authentication.getUser(github)
		if user != None:
			editedItem = database_access.getMenuItem(menu_id)
			if request.method == 'POST':
				editedItem.name = request.form['name']
				editedItem.description = request.form['description']
				editedItem.price = request.form['price']
				editedItem.course = request.form['course']
				database_access.updateMenuItem(editedItem)
				message = "%s Updated!" % editedItem.name
				flash(message)
				return redirect(url_for('showMenu', restaurant_id = restaurant_id))
			else:
				return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)
		else:
			return redirect(url_for('login'))		
	except TemplateNotFound:
		abort(404)		
	except Exception:
		abort(500)

#Delete a restaurant
@app.route('/restaurants/<int:restaurant_id>/delete', methods = ['GET','POST'])
def deleteRestaurant(restaurant_id):
	try:
		user = authentication.getUser(github)
		if user != None:
			restaurantToDelete = database_access.getRestaurant(restaurant_id)
			if request.method == 'POST':
				database_access.deleteRestaurant(restaurantToDelete)
				message = "%s Deleted!" % restaurantToDelete.name
				flash(message)
				return redirect(url_for('showRestaurants', restaurant_id = restaurant_id))
			else:
				return render_template('deleteRestaurant.html',restaurant = restaurantToDelete)
		else:
			return redirect(url_for('login'))
	except TemplateNotFound:
		abort(404)
	except Exception:
		abort(500)

#Delete a menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	try:
		user = authentication.getUser(github)
		if user != None:
			itemToDelete = database_access.getMenuItem(menu_id)
			if request.method == 'POST':
				database_access.deleteMenuItem(itemToDelete)
				message = "%s Deleted!" % itemToDelete.name
				flash(message)
				return redirect(url_for('showMenu', restaurant_id = restaurant_id))
			else:
				return render_template('deleteMenuItem.html', item = itemToDelete)
		else:
			return redirect(url_for('login'))		
	except TemplateNotFound:
		abort(404)
	except Exception:
		abort(500)		

if __name__ == '__main__':
	app.secret_key = '@123(^0(%'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)