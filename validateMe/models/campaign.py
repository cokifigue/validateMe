import Coupon

class Campaign():


	def __init__(self, name, max_uses_per_code, expiry_date, desc, number_of_codes=0):
		self.name = name
		self.max_uses_per_code = max_uses_per_code
		self.expiry_date = expiry_date
		self.desc = desc
		self.number_of_codes = number_of_codes
		self.coupons = [];

	def generate_new_coupons(self, num_to_generate=1):
		# generates coupons for this campaign, default 1

	def add_new_coupons(self, coupon_code_list):
		# generates coupons for this campaign, using the codes in the list.

	#Gets the list of coupons for this campaign
	def get_coupons(self):
		return self.coupons

	
		
	def serialize(self):
        return {
            'name': self.name, 
            'maxUsesPerCode': self.max_uses_per_code,
            'expiryDate': self.expiryDate,
            'desc': self.desc,
            'number_of_codes': self.number_of_codes
        }

