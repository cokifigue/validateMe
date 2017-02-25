from flask import Flask
from flask import request
from flask import jsonify
import random

app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World!"


@app.route("/campaign", methods=['POST'])
def campaign_post():
	json = request.get_json()
	return create_campaign_object(json)

def create_campaign_object(json):
	campaign_name = json['name']
	campaign_desc = json['desc']
	max_num_uses = json['maxNumUses']
	expiring_date = json['expiringDate']
	num_codes = json['numCodes']
	code_list = []
	# campaign = Campaign(campaign_name, max_num_uses, expiring_date, campaign_desc, num_codes)
	if 'codeList' in json:
		code_list = json['codeList']
		#campaign.add_new_coupons(code_list)
	# else:
	# 	campaign.generate_new_coupons(num_codes)
	# return jsonify(couponList=campaign.get_coupons())
	return jsonify(campaign_name=campaign_name, campaign_desc=campaign_desc)

@app.route("/campaign", methods=['GET'])
def campaign_get():
	# list_of_campaigns = campaign_manager.get_all_campaigns()
	# return jsonify(campaigns=[e.serialize() for e in list_of_campaigns])
	return jsonify(campaigns="future list of campaigns")


@app.route('/campaign/<campaign_id>')
def campaign_get_from_id(campaign_id):
    # show the user profile for that user
    # campaign = campaign_manage.get_campaign(campaign_id)
    # return jsonify(campaign = campaign.serialize())
    return jsonify(campaignId=campaign_id)

if __name__ == "__main__":
	app.run(debug=True)

