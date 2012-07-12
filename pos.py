import webapp2
import jinja2
import os
from ProductEntity import *
from Terminal import *

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


# Front page handler
class TerminalPage(BaseHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.render('terminal.html')

	def post(self):
		pass

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