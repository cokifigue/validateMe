from flask import request
from flask import jsonify
from datetime import datetime
import json
import random

from models.campaign import Campaign
from models.coupon import Coupon
from validateMe import app
from validateMe import db


@app.before_first_request
def setup():
    # Recreate database each time for demo
    db.drop_all()
    db.create_all()
    
def create_campaign_from_json(json):
    campaign = Campaign(json['name'], json['maxNumUses'], json['expirationDate'], json['desc'], json['numCodes'])
    print json
    if 'codeList' in json:
    	print 'there is list'
        code_list = json['codeList']
        campaign.add_new_coupons(code_list)
    else:
        campaign.generate_new_coupons(json['numCodes'])
    return campaign

@app.route("/")
def hello():
    return "Hello World!"

# POST: Create campaign 
@app.route("/campaign", methods=['POST'])
def post_campaign():
    input_json = request.get_json()
    campaign = create_campaign_from_json(input_json)
    db.session.add(campaign)
    db.session.commit()
    return jsonify(campaigns=campaign.serialize())

# GET: Get campaign info
@app.route("/campaign", methods=['GET'])
def get_all_campaigns():
    list_of_campaigns = Campaign.query.all()
    return jsonify(campaigns=[e.serialize() for e in list_of_campaigns])

# GET: Get campaign info for specific campaign
@app.route('/campaign/<int:campaign_id>')
def get_campaign_from_id(campaign_id):
    campaign = Campaign.query.filter_by(id=campaign_id).first()
    return jsonify(campaign = campaign.serialize())

# GET: Ends campaign and returns campaign info with new expiration date for codes
@app.route('/campaign/<int:campaign_id>/end_campaign')
def end_campaign(campaign_id):
    campaign = Campaign.query.filter_by(id=campaign_id).first()
    campaign.update_expiration_date(datetime.now())
    return jsonify(campaign = campaign.serialize())

# GET: Get list of codes for specific campaign
@app.route('/campaign/<campaign_id>/codes')
def get_codes_from_campaign_id(campaign_id):
    campaign = Campaign.query.filter_by(id=campaign_id).first()
    return jsonify(coupons=[c.serialize() for c in campaign.coupons])

# GET: Validate specific coupon code, returns Boolean
@app.route('/validate/<coupon_code>')
def validate_code(coupon_code):
    coupon = Coupon.query.filter_by(code=coupon_code).first()
    campaign = Campaign.query.filter_by(id=coupon.campaign_id).first()
    if not coupon:
        return jsonify(valid=False)
    return jsonify(valid=coupon.isValid(campaign))

# GET: Redeem coupon code, returns Boolean 
@app.route('/redeem/<coupon_code>')
def redeem_code(coupon_code):
    coupon = Coupon.query.filter_by(code=coupon_code).first()
    campaign = Campaign.query.filter_by(id=coupon.campaign_id).first()
    if not coupon:
        return jsonify(seccess=False, error="No such code")

    try:
        coupon.redeem(campaign)
        return jsonify(success=True, error=None)
    except Exception as e:
        return jsonify(success=False, error=e.message)



