# coding=utf-8
"""
The Offers endpoint

Documentation: https://developer.allegro.pl/documentation/#/
Schema:
"""
from __future__ import unicode_literals

from ..base import BaseApi
from .offerrenewcommands import OfferRenewCommands
from .offerchangepricecommands import OfferChangePriceCommands


class Offers(BaseApi):
    """
    Base Endpoint
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(Offers, self).__init__(*args, **kwargs)
        self.endpoint = 'offers'
        self.change_price_commands = OfferChangePriceCommands(self)
        self.renew_commands = OfferRenewCommands(self)
