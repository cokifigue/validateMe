from flask import request
from flask import jsonify
import random

from models.campaign import Campaign
from models.coupon import Coupon
from validateMe import app


@app.before_first_request
def setup():
    # Recreate database each time for demo
    db.create_all()
    
def create_campaign_from_json(json):
	campaign = Campaign(json['name'], json['maxNumUses'], 
						json['expiringDate'], json['desc'], 
						json['num_codes'])
	if 'codeList' in json:
		code_list = json['codeList']
		campaign.add_new_coupons(code_list)
	else:
	 	campaign.generate_new_coupons(num_codes)
	return campaign

@app.route("/")
def hello():
	return "Hello World!"


#@app.route("/save_test")
#def save():
#	campaign = Campaign()
#	return "Hello World!"
#
#@app.route("/load_test")
#def load():
#	return "Hello World!"
#

@app.route("/campaign", methods=['POST'])
def post_campaign():
	json = request.get_json()
	campaign = create_campaign_from_json(json)
	return jsonify(couponList=campaign.get_coupons())

@app.route("/campaign", methods=['GET'])
def get_all_campaigns():
	# list_of_campaigns = campaign_manager.get_all_campaigns()
	# return jsonify(campaigns=[e.serialize() for e in list_of_campaigns])
	return jsonify(campaigns="future list of campaigns")

@app.route('/campaign/<campaign_id>')
def get_campaign_from_id(campaign_id):
    # campaign = campaign_manage.get_campaign(campaign_id)
    # return jsonify(campaign = campaign.serialize())
    return jsonify(campaignId=campaign_id)

@app.route('/campaign/<campaign_id>/codes')
def get_codes_from_campaign_id(campaign_id):
    # campaign = campaign_manage.get_campaign(campaign_id)
    # return jsonify(couponList=campaign.get_coupons())
    return jsonify(campaignId=campaign_id)

@app.route('/validate/<code>')
def validate_code(code):
    # campaign = campaign_manage.get_campaign(campaign_id)
    # return jsonify(couponList=campaign.get_coupons())
    return jsonify(campaignId=campaign_id)

@app.route('/redeem/<code>')
def redeem_code(code):
    # campaign = campaign_manage.get_campaign(campaign_id)
    # return jsonify(couponList=campaign.get_coupons())
    return jsonify(campaignId=campaign_id)