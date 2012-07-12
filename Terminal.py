from ProductModel import *

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
			item = Product.get(sku)
			if not item:
				Product.insert(sku=sku, product=product)
				return True
			else:
				return False

	def delete_product(self, sku=None):
		return Product.delete(sku)
