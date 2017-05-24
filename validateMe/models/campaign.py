from coupon import Coupon
from hashids import Hashids
from random import randint
from validateMe import db
from datetime import datetime

class Campaign(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	max_uses_per_code = db.Column(db.Integer)
	expiry_date = db.Column(db.String(100))
	desc = db.Column(db.String(100))
	number_of_codes = db.Column(db.Integer)
	#coupons = db.relationship('Coupon', backref='campaign',
	#	lazy='dynamic')

	# def __init__(self, name, max_uses_per_code, expiry_date, desc, number_of_codes=0):
	# 	self.name = name
	# 	self.max_uses_per_code = max_uses_per_code
	# 	self.expiry_date = expiry_date
	# 	self.desc = desc
	# 	self.number_of_codes = number_of_codes
	# 	#self.coupons = [];

	def generate_new_coupons(self, num_to_generate=1):
		code_list = []
		for i in range(num_to_generate):
			code_list.append(generate_code())
		return code_list
	
	def generate_code(self):
		rand1 = randint(0,999)
		rand2 = randint(0,999)
		rand3 = randint(0,999)
		#id=campaign_id
		hashids = Hashids(rand1,rand2,rand3)#id)

	#Gets the list of coupons for this campaign
	def get_coupons(self):
		return self.coupons
	

	def add_new_coupons(self, coupon_code_list):
	# generates coupons for this campaign, using the codes in the list.
		return None


	def serialize(self):
		return {'name': self.name, 
				'maxUsesPerCode': self.max_uses_per_code,
				'expiryDate': self.expiryDate,
				'desc': self.desc,
				'number_of_codes': self.number_of_codes}

