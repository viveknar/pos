from google.appengine.ext import db

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
			p = cls.get(sku)
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
