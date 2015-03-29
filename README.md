# Item Catalog #

*	Contributors: Rudi Jonker
*	Requires at least: Python 2.7
*	Requires at least: Vagrant
*	Requires at least: SQLAlchemy
*	Requires at least: Flask
*	Requires at least: GitHub-Flask
*	Requires at least: rauth
*	Requires at least: User Account with GitHub


### Overview ###
*	A website to allow you to create a restaurant and a menu for that restaurant
*	Multiple restaurants can be created

### Using the Source Code ###

*	Clone item_catalog. Source code is found in 'catalog' folder
*	Install Vagrant and VirtualBox (https://www.udacity.com/wiki/ud197/install-vagrant)
*	Launch the Vagrant VM (vagrant up)
*	Within the VM, execute the database_setup.py file. A restaurantmenu.db should be created
*	Within the VM, execute the restaurant_webserver.py file to start the web server
*	Access the website using http://localhost:5000/

### Authentication ###
*	To perform any functions, you will need to get authorized using your GitHub user account

### Create A Restaurant ###
*	Click the link to create a restaurant. A restaurant name is required

### Create A Restaurant's Menu ###
*	Click the link to create a menu item. All fields are required
*	Price field requires a valid decimal number with TWO (2) decimal places

### Installation ###

*	Git
	*	git clone https://github.com/rjonker1/item_catalog.git
*	Files
	*	Files are found in catalog folder
