from ProductModel import *
from ProductEntity import *
import json

from google.appengine.api import memcache	
import logging

''' 
Terminal class representing the point of sales to scan items
'''
class Terminal:
	def __init__(self, items_list={}):
		self._items_list = items_list

	'''
	Return a list of all items in the checkout item list
	'''
	def get_item_list(self):
		return self._items_list

	'''
	Get the product details for a product given a product SKU
	'''
	def get_product_details(self, sku):
		# TODO: Implement some sort of caching system (memcache) to cut down frequent requests
		# being made to the database
		p = Product.get(sku)
		if p is not None:
			data = p.product
			memcache.set(sku, data)
			return json.loads(data)
	
	'''
	Scan items and add it to the item list to compute the total price
	'''
	def scan(self, sku):
		if sku in self._items_list:
			self._items_list[sku] += 1
		else:
			self._items_list[sku] = 1
	
	'''
	Calculate the total price of an item based on the quantity purchased. If 
	volume price is set, then calculate based on the volume price.
	'''
	def calculate_price(self, sku, count):
		try:
			entity = self.get_product_details(sku)
			product = ProductEntity().load_json(entity)
			unit_price = float(product.get_unit_price()[1:])
			bulk_count = product.get_bulk_quantity()
			bulk_price = product.get_bulk_price()[1:]
			
			if bulk_count and bulk_price:
				bulk_count = float(bulk_count)
				bulk_price = float(bulk_price)
				diff = 0
				if count >= bulk_count:
					diff = count - bulk_count
					return (diff * unit_price) + bulk_price
				else:
					return count * unit_price
			else:
				return count * unit_price
		except:
			return 0.00
		
	'''
	Set the price for an item. Item prices can only be set when correctly authenticated 
	to ensure only managers and store people can set prices.
	'''
	def set_price(self, authenticated=False, DBNames=[], sku=None, unit_price=None, bulk_quantity=None, bulk_price=None, currency='$'):
		if authenticated and sku and unit_price:
			try:
				entity = self.get_product_details(sku)
			except:
				return False
			product = ProductEntity().load_json(entity)
			product.set_unit_price(unit_price, currency=currency)
			
			if bulk_price:
				product.set_bulk_price(bulk_price, currency=currency)
			if bulk_quantity:
				product.set_bulk_quantity(bulk_quantity)
			status = product.update(DBNames)
			
			return status
		return False

	'''
	Calculate the total price for all the items present in the checkout item list.
	'''
	def total_price(self):
		total = 0.00
		for sku, count in self._items_list.iteritems():
			total += self.calculate_price(sku, count)
		self._items_list.clear()
		return total

	'''
	Get a list of all the items in the inventory along with product codes and description.
	'''
	def get_inventory(self):
		items = Product.all()
		return items


