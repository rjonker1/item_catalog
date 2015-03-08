items = session.query(MenuItem).all()
for item in items


veggieBurgers = session.query(MenuItem).filter_by(name = "Veggie Burger")
for veggieBurger in veggieBurgers:
	for veggieBurger in veggieBurgers:
	print veggieBurger.id
	print veggieBurger.Price
	print veggiBurger.restaurant.name
	print "\n"

urbanBurger = session.query(MenuItem).filter_by(id = 8).one()

#update the Price
urbanBurger.price = "R2.00"
session.add(urbanBurger)
session.commit()


for veggieBurger in veggieBurgers
	if veggieBurger.price != "$2.99":
		veggieBurger.price = "$2.99"
		session.add(veggieBurger)
		session.commit()

#deleting
#delete an ice cream....

#1. Find entry
#

iceCream = session.query(MenuItem).filter_by(name = "Spinach Ice Cream").one()
session.delete(iceCream)
session.commit()