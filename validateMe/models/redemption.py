from validateMe import db
from datetime import datetime

class Redemption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupon.id'))
    redemption_date = db.Column(db.DateTime)

    def __init__(self):
        self.redemption_date = datetime.now()

    def serialize(self):
        return {'coupon' : self.coupon.serialize(),
                'redemption_date': self.redemption_date}