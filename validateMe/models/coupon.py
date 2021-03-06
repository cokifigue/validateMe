from validateMe import db
from redemption import Redemption

class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    uses_remaining = db.Column(db.Integer)
    code = db.Column(db.String(80))
    redemptions = db.relationship('Redemption', backref='coupon', lazy='dynamic')

    def __init__(self, code, uses_remaining):
        self.code = code
        self.uses_remaining = uses_remaining

    def is_valid(self):
        # verify that this coupon has remaining uses
        return self.campaign.is_active() and self.uses_remaining > 0

    def redeem(self):
        # check if this coupon is valid
        if not self.is_valid():
            raise ValueError('This coupon is no longer valid')

        # redeem this coupon
        try:
            # reduce the number of remaining uses
            self.uses_remaining -= 1

            # create a new redemption record
            redemption = Redemption()
            self.redemptions.append(redemption)
            db.session.add(redemption)

            # commit changes
            db.session.commit()
        except Exception as e:
            raise e

    def serialize(self):
        return {'code' : self.code,
                'uses_remaining': self.uses_remaining,
                'campaign_id': self.campaign.id}
