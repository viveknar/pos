import webapp2
import jinja2
import os
import hashlib
from ProductEntity import *
from Terminal import *
from ProductModel import *
import json


templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(templates_dir), autoescape = True)


def is_number(number):
	try:
		float(number)
		return True
	except:
		return False

class BaseHandler(webapp2.RequestHandler):
	def write(self, *a, **ka):
		self.response.out.write(*a, **ka)

	def render_string(self, template, **ka):
		t = jinja_env.get_template(template)
		return t.render(ka)

	def render(self, template, **ka):
		return self.write(self.render_string(template, **ka))

	def render_json(self, a):
		json_txt = json.dumps(a)
		self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
		self.write(json_txt)

class MainPage(BaseHandler):
	def get(self):
		self.redirect('/pos')

# Front page handler
class TerminalPage(BaseHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.render('terminal.html')


	def post(self):
		terminal = Terminal()
		scanned_items = self.request.get('scanned_items')

		items = scanned_items.split(',')
		for item in items:
			terminal.scan(item)
		total_price = terminal.total_price()
		
		self.render('terminal.html', scanned_items=scanned_items, total=str(total_price))

class NewProductPage(BaseHandler):
	def get(self):
		self.render('new_product.html')

	def post(self):
		sku = self.request.get('sku')
		name = self.request.get('name')
		unit_price = self.request.get('unit_price')
		bulk_quantity = self.request.get('bulk_quantity')
		bulk_price = self.request.get('bulk_price')
		description = self.request.get('description')
		inventory_count = '100'

		p = ProductEntity(
					sku = sku, 
					name = name,
					unit_price = unit_price,
					bulk_quantity = bulk_quantity,
					bulk_price = bulk_price,
					description = description,
					inventory_count = inventory_count
				)
		if p.insert():
			self.write(p.build_json())
		else:
			self.write("error")

class DeleteProductPage(BaseHandler):
	def get(self):
		self.render('delete_product.html')

		sku = self.request.get('sku')
		all_entries = self.request.get('all_entries')
		
		if all_entries.lower() == 'true':
			ProductEntity().delete(all_entries=True)
			self.write("Items deleted")
		else:
			if sku:
				details = Terminal().get_product_details(sku)
				p = ProductEntity().load_json(details)
				p.delete()

class SetPricePage(BaseHandler):
	def get(self):
		self.render('set_price.html')

	def post(self):
		terminal = Terminal()
		
		if len(self.request.arguments()) == 0 or not self.request.get('sku') or not self.request.get('unit_price'):
			self.render('set_price.html')
		else:
			sku = self.request.get('sku')
			unit_price = self.request.get('unit_price')
			bulk_price = self.request.get('bulk_price')
			bulk_quantity = self.request.get('bulk_quantity')
			if terminal.get_product_details(sku):
				terminal.set_price(sku, unit_price=unit_price, bulk_price=bulk_price, bulk_quantity=bulk_quantity)
				self.write(json.dumps(terminal.get_product_details(sku)))
			else:
				self.write("item not found")

class DataStorePage(BaseHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
		items = Product.get_inventory()
		item_list = []
		for item in items:
			item_list.append(json.loads(item.product))

		self.render_json(item_list)


app = webapp2.WSGIApplication([('/pos/?', TerminalPage),
								('/?', MainPage),
								('/pos/newproduct/?', NewProductPage),
								('/pos/deleteproduct/?', DeleteProductPage),
								('/pos/setprice/?', SetPricePage),
								('/pos/datastore/?', DataStorePage)], debug = True)