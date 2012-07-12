# Class to describe each items properties
import json

class ProductEntity:
	
	def __init__(self, **kw):
		self._sku = kw['sku']
		self._name = kw['name']
		self._unit_price = kw['unit_price']
		self._description = kw['description']

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

	def set_unit_price(self, unit_price):
		self._unit_price = unit_price

	def get_description(self):
		return self._description

	def set_description(self, description):
		self._description = description

	def build_json_blob(self):
		json_object = {}
		
		data = {
			"name" : self.get_name(),
			"unit_price" : self.get_unit_price(),
			"description" : self.get_description()
		}

		json_object = {
			"sku" : self.get_sku(),
			"data" : data
		}
		return json.dumps(json_object)