from google.appengine.ext import db

'''
The Product model representing the Product table
'''

class Product(db.Model):
	'''
	fields in the table
	'''
	sku = db.StringProperty(required = True)
	product = db.TextProperty(required = True)

	'''
	Insert to database
	'''
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
	'''
	Delete from database
	'''
	@classmethod
	def delete(cls, sku=None, all_entries=False):
		if all_entries:
			flag = False
			q = Product.all()
			for entry in q:
				try:
					db.delete(entry.key())
				except:
					return False
			flag = True
			return flag
		else:
			if sku:
				p = cls.get(sku)
				try:
					db.delete(p.key())
					return True
				except:
					return False
		
	'''
	select from database
	'''				
	@classmethod
	def get(cls, sku):
		item = None
		if sku:
			try:
				q = db.Query(Product)
				q.filter('sku =', sku)
				item = q.get()
			except:
				pass
		return item

	'''
	Update database entry
	'''	
	@classmethod
	def update(cls, entity):
		try:
			entity.put()
			return True
		except:
			return False

	@classmethod
	def get_inventory(cls):
		items = Product.all()
		return items



