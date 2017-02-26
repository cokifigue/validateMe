class Coupon():
	def __init__(self, code, campaign_id, uses_remaining):
		self.code = code
		self.campaign_id = campaign_id
		self.uses_remaining = uses_remaining

	def isValid(self):
		# verify that this coupon has remaining uses
		if self.uses_remaining <= 0:
			return False

		# verify that this coupon's campaign has not expired
		# TODO

		return True


	def redeem(self):
		# check if this coupon is valid
		if self.isValid == False:
			raise ValueError('This coupon is no longer valid')

		# redeem this coupon
		self.uses_remaining -= 1
