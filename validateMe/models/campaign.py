from coupon import Coupon
from hashids import Hashids
from random import randint
from validateMe import db
from datetime import datetime
from time import strftime
from sqlalchemy.sql import exists


class Campaign(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	max_uses_per_code = db.Column(db.Integer)
	expiration_date = db.Column(db.String(100))
	desc = db.Column(db.String(100))
	number_of_codes = db.Column(db.Integer)
	coupons = db.relationship('Coupon', backref='campaign',	lazy='dynamic')

	def __init__(self, name, max_uses_per_code, expiration_date, desc, number_of_codes=0):
		self.name = name
		self.max_uses_per_code = max_uses_per_code
		self.expiration_date = expiration_date
		self.desc = desc
		self.number_of_codes = number_of_codes
		self.coupons = [];

	
	def generate_code(self):
		rand1 = randint(0,999)
		rand2 = randint(0,999)
		rand3 = randint(0,999)
		hashids = Hashids()
		hashid = hashids.encode(rand1, rand2, rand3)
		return hashid

	def generate_new_coupons(self, num_to_generate=1):
		for i in range(num_to_generate):
			self.create_coupon(self.generate_code(), self.max_uses_per_code)
			
	def add_new_coupons(self, coupon_code_list):
		for code in coupon_code_list:
			self.create_coupon(code, self.max_uses_per_code)

	def create_coupon(self, code, max_uses):
		if not db.session.query(exists().where(Coupon.code == code)).scalar():
			coupon = Coupon(code, max_uses)
			self.coupons.append(coupon)
			db.session.add(coupon)
			db.session.commit()

	def update_expiration_date(self, new_expiration_date):
		self.expiration_date = new_expiration_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
		db.session.commit()

	def is_active(self):
		# Example of expected time format 2017-08-31T18:25:43.511Z
		datetime_object = datetime.strptime(self.expiration_date, '%Y-%m-%dT%H:%M:%S.%fZ')
		return datetime.now() <= datetime_object

	def serialize(self):
		return {'id' : self.id,
				'name': self.name, 
				'maxUsesPerCode': self.max_uses_per_code,
				'expirationDate': self.expiration_date,
				'desc': self.desc,
				'number_of_codes': self.number_of_codes,
				'coupons': [c.serialize() for c in self.coupons]}

