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
	if 'codeList' in json:
		code_list = json['codeList']
	else:
		code_list = [] #generate_codes(num_codes)
	# return Campaign(campaign_name, campaign_desc, max_num_uses, expiring_date,num_codes, code_list)
	return jsonify(campaign_name=campaign_name, campaign_desc=campaign_desc)

if __name__ == "__main__":
	app.run(debug=True)


#Campaign Name
# Campaign Description
# Max # uses per code
# Expiring date
# Number of Codes
# List of Codes
