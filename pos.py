import webapp2
import jinja2
import os
from ProductEntity import *
from google.appengine.ext import db

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(templates_dir), autoescape = True)

class BaseHandler(webapp2.RequestHandler):
	def write(self, *a, **ka):
		self.response.out.write(*a, **ka)

	def render_string(self, template, **ka):
		t = jinja_env.get_template(template)
		return t.render(ka)

	def render(self, template, **ka):
		return self.write(self.render_string(template, **ka))


# The Product model representing the Product table
class Product(db.Model):
	sku = db.StringProperty(required = True)
	product = db.TextProperty(required = True)

	@classmethod
	def insert(cls, **kw):
		sku = kw['sku']
		product = kw['product']
		try:
			p = Product(sku=sku, product=product)
			p.put()
			return True
		except:
			return False

	@classmethod
	def delete(cls, sku=None):
		if sku:
			p = cls.get_product(sku)
			try:
				db.delete(p.key())
				return True
			except:
				return False
		else:
			flag = False
			q = Product.all()
			for entry in q:
				try:
					db.delete(entry.key())
					flag = True
					break
				except:
					pass
			return flag

	@classmethod
	def get_product(cls, sku):
		item = None
		if sku:
			try:
				q = db.Query(Product)
				q.filter('sku =', sku)
				item = q.get()
			except:
				pass
		return item

# Terminal class representing the point of sales to scan items
class Terminal:
	def scan(self, product_id):
		pass

	def set_pricing(self, sku, product_price):
		pass

	def new_product(self, **ka):
		sku = ka['sku']
		product = ka['product']
		if sku and product:
			item = Product.get_product(sku)
			if not item:
				Product.insert(sku=sku, product=product)
				return True
			else:
				return False

	def delete_product(self, sku=None):
		return Product.delete(sku)

# Front page handler
class TerminalPage(BaseHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.render('terminal.html')

	def post(self):
		terminal = Terminal()
		self.write(terminal.new_product(sku="123456", product="apples"))
		self.write(terminal.new_product(sku="123457", product="oranges"))
		#self.write(terminal.delete_product())
class NewProductPage(BaseHandler):
	def get(self):
		self.render('new_product.html')

	def post(self):
		sku = self.request.get('sku')
		name = self.request.get('name')
		unit_price = self.request.get('unit_price')
		description = self.request.get('description')

		p = ProductEntity(
					sku = sku, 
					name = name,
					unit_price = unit_price,
					description = description
				)
		product = p.build_json_blob()
		terminal = Terminal()
		if terminal.new_product(sku=sku, product=product):
			self.write(product)
		else:
			self.write("error")

class DeleteProductPage(BaseHandler):
	def get(self):
		self.render('delete_product.html')

		sku = self.request.get('sku')
		if sku:
			terminal = Terminal()
			if sku == 'ALL_ENTRIES':
				terminal.delete_product()
				self.write("Items deleted")
			else:
				terminal.delete_product(sku)

app = webapp2.WSGIApplication([('/pos', TerminalPage),
								('/pos/newproduct', NewProductPage),
								('/pos/deleteproduct', DeleteProductPage)], debug = True)