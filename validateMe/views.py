from flask import request
from flask import jsonify
import random
import json

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
    campaign = Campaign(json['name'], json['maxNumUses'], json['expiringDate'], json['desc'], json['numCodes'])
    print json
    if 'codeList' in json:
        code_list = json['codeList']
        campaign.add_new_coupons(code_list)
    else:
        campaign.generate_new_coupons(json['numCodes'])
    return campaign

@app.route("/")
def hello():
    return "Hello World!"


#@app.route("/save_test")
#def save():
#   campaign = Campaign()
#   return "Hello World!"
#
#@app.route("/load_test")
#def load():
#   return "Hello World!"
#

@app.route("/campaign", methods=['POST'])
def post_campaign():
    input_json = request.get_json()
    campaign = create_campaign_from_json(input_json)
    db.session.add(campaign)
    db.session.commit()
    return jsonify(campaigns=campaign.serialize())

@app.route("/campaign", methods=['GET'])
def get_all_campaigns():
    list_of_campaigns = Campaign.query.all()
    return jsonify(campaigns=[e.serialize() for e in list_of_campaigns])

@app.route('/campaign/<int:campaign_id>')
def get_campaign_from_id(campaign_id):
    campaign = Campaign.query.filter_by(id=campaign_id).first()
    return jsonify(campaign = campaign.serialize())

@app.route('/campaign/<campaign_id>/codes')
def get_codes_from_campaign_id(campaign_id):
    campaign = Campaign.query.filter_by(id=campaign_id).first()
    return jsonify(coupons=[c.serialize() for c in campaign.coupons])

@app.route('/validate/<coupon_code>')
def validate_code(coupon_code):
    coupon = Coupon.query.filter_by(code=coupon_code).first()
    if not coupon:
        return jsonify(valid=False)
    return jsonify(valid=coupon.isValid())

@app.route('/redeem/<coupon_code>')
def redeem_code(coupon_code):
    coupon = Coupon.query.filter_by(code=coupon_code).first()

    if not coupon:
        return jsonify(seccess=False, error="No such code")

    try:
        coupon.redeem()
        return jsonify(success=True, error=None)
    except Exception as e:
        return jsonify(success=False, error=e.message)



