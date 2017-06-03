from validateMe import db
from datetime import datetime

class Coupon(db.Model):
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    uses_remaining = db.Column(db.Integer)
    code = db.Column(db.String(80), primary_key=True)

    def __init__(self, code, uses_remaining):
        self.code = code
        self.uses_remaining = uses_remaining


    def isValid(self, campaign):
        # verify that this coupon has remaining uses
        if self.uses_remaining <= 0:
            return False

        # Example of expected time format 2017-08-31T18:25:43.511Z
        datetime_object = datetime.strptime(campaign.expiration_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        print datetime_object
        return datetime.now() <= datetime_object

    def redeem(self, campaign):
        # check if this coupon is valid
        if not self.isValid(campaign):
            raise ValueError('This coupon is no longer valid')

        # redeem this coupon
        try:
            self.uses_remaining -= 1
            db.session.commit()
        except Exception as e:
            raise e

    def serialize(self):
        return {'code' : self.code,
                'uses_remaining': self.uses_remaining,
                'campaign_id': self.campaign.id}
