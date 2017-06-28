from flask_restplus import fields
from validateMe import api

coupon = api.model('Coupon', {
    'campaign_id': fields.Integer(description='Campaign Id'),
    'uses_remaining': fields.Integer(required=True, description='Number of uses remaining for coupon'),
    'code': fields.String(description='Coupon code String')
})

campaign = api.model('Campaign', {
    'name': fields.String(required=True, description='Campaign Name', default=""),
    'max_uses_per_code': fields.Integer(description='Max number of uses per coupon', default=1),
    'expiration_date': fields.DateTime(description='Expiration date for campaign'),
    'desc': fields.String(description='Campaign description', default=""),
    'number_of_codes': fields.Integer(required=True, default=5, description='Number of codes to create'),
    'coupons': fields.List(fields.Nested(coupon), default=[], description='List of coupons (optional)')
})
