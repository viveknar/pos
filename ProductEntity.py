# Class to describe each items properties
import json
from ProductModel import *

class ProductEntity:
	
	'''
	Setting all properties for a product when it is being instatiated.
	'''
	def __init__(self, **kw):
		if kw:
			self._sku = kw['sku']
			self._name = kw['name']
			if kw['unit_price']:
				self._unit_price = self.convert_to_currency(kw['unit_price'], kw['currency'])
			else:
				self._unit_price = ''

			self._bulk_quantity = kw['bulk_quantity']
			if kw['bulk_price']:
				self._bulk_price = self.convert_to_currency(kw['bulk_price'], kw['currency'])
			else:
				self._bulk_price = ''
			self._description = kw['description']
		else:
			self._sku = ''
			self._name = ''
			self._unit_price = ''
			self._bulk_quantity = ''
			self._bulk_price = ''
			self._description = ''

	'''
	Giving an option to set currency. The same product can be sold across different countries, and this 
	makes storing prices for different regions easy. The default currency is set to USD
	'''
	def convert_to_currency(self, number, currency='$'):
		try:
			c = currency+'{:,.2f}'.format(float(number))
		except:
			c = currency+'0.00'
		return c
		
	'''
	Bunch of getter and setter methods to access all the private members of each product entity
	'''
	def get_sku(self):
		return self._sku

	def set_sku(self, sku):
		self._sku = sku

	def get_name(self):
		return self._name

	def set_name(self, name):
		self._name = name

	def get_unit_price(self):
		return self._unit_price

	def set_unit_price(self, unit_price, currency='$'):
		self._unit_price = self.convert_to_currency(unit_price, currency)

	def get_bulk_quantity(self):
		return self._bulk_quantity

	def set_bulk_quantity(self, bulk_quantity):
		self._bulk_quantity = bulk_quantity

	def get_bulk_price(self):
		return self._bulk_price

	def set_bulk_price(self, bulk_price, currency='$'):
		self._bulk_price = self.convert_to_currency(bulk_price, currency)

	def get_description(self):
		return self._description

	def set_description(self, description):
		self._description = description

	'''
	Function to insert the product into the database. Additional feature to add product to any database 
	mentioned in DBNames. 
	This is to show that the same product could be inserted to multiple databases located in multiple locations
	'''
	def insert(self, DBNames=[]):
		if len(DBNames) > 0:		
			for DBName in DBNames:
				sku = self._sku
				product = self.build_json()
				if sku and product:
					item = DBName.get(sku)
					if not item:
						DBName.insert(sku=sku, product=product)
						return True
					else:
						return False
		return False
	'''
	Update a product entry in multiple databases
	'''
	def update(self, DBNames=[]):
		if len(DBNames) > 0:
			for DBName in DBNames:
				sku = self._sku
				product = self.build_json()
				item = DBName.get(sku)
				if item:
					item.product = product
					return DBName.update(item)
				return False
		return False
	'''
	Delete the product from the database
	'''
	def delete(self, DBNames=[]):
		if len(DBNames) > 0:
			for DBName in DBNames:
				status = Product.delete(sku=self._sku)
				if status is False:
					return False
		return True

	'''
	Each product is stored as a JSON object representing all features of the product. This way the API can
	be easily integrated with a RESTful API. 
	'''
	def build_json(self):
		json_object = {}
		
		bulk = {
			"quantity" : self.get_bulk_quantity(),
			"price" : self.get_bulk_price()
		}

		data = {
			"name" : self.get_name(),
			"unit_price" : self.get_unit_price(),
			"bulk" : bulk,
			"description" : self.get_description()
		}

		json_object = {
			"sku" : self.get_sku(),
			"data" : data
		}
		return json.dumps(json_object)

	'''
	Loads a json string representing product into a ProductEntity object
	'''
	def load_json(self, product):
		self._sku = product['sku']
		self._name = product['data']['name']
		self._unit_price = product['data']['unit_price']
		self._bulk_quantity = product['data']['bulk']['quantity']
		self._bulk_price = product['data']['bulk']['price']
		self._description = product['data']['description']
		return self