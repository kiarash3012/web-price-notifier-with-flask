import uuid
import datetime
import src.models.alerts.constants as AlertConstants
from sparkpost import SparkPost
from src.models.items.item import Item

from src.common.database import Database


class Alert(object):
    def __init__(self, user_email, price_limit, item_id, last_checked=None, _id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Alert for {} on item {} with price {}>".format(self.user_email, self.item, self.perice_limit)

    def send(self):
        sparky = SparkPost(AlertConstants.API_KEY)
        return sparky.transmission.send(
            use_sandbox=True,
            recipients=self.user_email.email,
            from_email='kiarash3012@gmail.com',
            subject='Price limit reached for {}'.format(self.item.name),
            html='<html><body><h3> we\'ve fuond a deal! (link here).</h3></body></html>'
        )

    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {'last_checked':
                                                                                      {'$lte': last_updated_limit}
                                                                                  })]

    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION, {'_id': self._id}, self.json())

    def json(self):
        return {
            '_id': self._id,
            'price_limit': self.price_limit,
            'last_checked': self.last_checked,
            'user_email': self.user_email,
            'item_id': self.item._id
        }

    def load_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        self.save_to_mongo()
        return self.item.price

    def sen_email_if_price_reached(self):
        if self.item.price < self.price_limit:
            self.send()