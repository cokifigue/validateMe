from flask import request
from flask import jsonify
from datetime import datetime
from flask_restplus import Resource
from api_models import coupon, campaign
import json
import random


from models.campaign import Campaign
from models.coupon import Coupon
from validateMe import app
from validateMe import db
from validateMe import api

campaign_ns = api.namespace('campaign', description='Operations related to campaign')
validate_ns = api.namespace('validate', description='Operations related to coupon validation')
redeem_ns = api.namespace('redeem', description='Operations related to coupon redemption')

@app.before_first_request
def setup():
    # Recreate database each time for demo
    db.drop_all()
    db.create_all()

    
def create_campaign_from_json(json):
    campaign = Campaign(json['name'], json['max_uses_per_code'], json['expiration_date'], json['desc'], json['number_of_codes'])
    print json
    if 'coupons' in json and len(json['coupons']) > 0:
        code_list = json['coupons']
        campaign.add_new_coupons(code_list)
    else:
        campaign.generate_new_coupons(json['number_of_codes'])
    return campaign


def get_valid_coupon(coupon_code):
	coupons = Coupon.query.filter_by(code=coupon_code)
	print coupons
	for coupon in coupons:
		if coupon.is_valid():
			return coupon
	return None


@app.route("/")
def hello():
    return "Hello World!"

@campaign_ns.route("/", methods=['GET', 'POST'])
class CampaignCollection(Resource):
    def get(self):
        list_of_campaigns = Campaign.query.all()
        return jsonify(campaigns=[e.serialize() for e in list_of_campaigns])

    @api.expect(campaign)
    def post(self):
        input_json = request.json
        campaign = create_campaign_from_json(input_json)
        db.session.add(campaign)
        db.session.commit()
        return jsonify(campaigns=campaign.serialize())



# GET: Get campaign info for specific campaign
@campaign_ns.route('/<int:campaign_id>')
class CampaignItem(Resource):
    def get(self, campaign_id):
        campaign = Campaign.query.filter_by(id=campaign_id).first()
        return jsonify(campaign = campaign.serialize())


# GET: Ends campaign and returns campaign info with new expiration date for codes
@campaign_ns.route('/<int:campaign_id>/end_campaign')
class EndCampaign(Resource):
    def get(self, campaign_id):
        campaign = Campaign.query.filter_by(id=campaign_id).first()
        campaign.update_expiration_date(datetime.now())
        return jsonify(campaign = campaign.serialize())


# GET: Get list of codes for specific campaign
@campaign_ns.route('/<int:campaign_id>/codes')
class CodeCollection(Resource):
    def get(self, campaign_id):
        campaign = Campaign.query.filter_by(id=campaign_id).first()
        return jsonify(coupons=[c.serialize() for c in campaign.coupons])


# GET: Validate specific coupon code, returns Boolean
@validate_ns.route('/<string:coupon_code>')
class ValidateCode(Resource):
    def get(self, coupon_code):
    	coupon = get_valid_coupon(coupon_code)
    	if coupon == None:
    		return jsonify(valid=False)
    	return jsonify(valid=coupon.is_valid())


# GET: Redeem coupon code, returns Boolean 
@redeem_ns.route('/<string:coupon_code>')
class RedeemCode(Resource):
    def get(self, coupon_code):
        coupon = get_valid_coupon(coupon_code)
        if coupon == None:
            return jsonify(success=False, error="No such code")

        try:
            coupon.redeem()
            return jsonify(success=True, error=None)
        except Exception as e:
            return jsonify(success=False, error=e.message)



