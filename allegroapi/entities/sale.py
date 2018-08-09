# coding=utf-8
"""
The Sale endpoint


Documentation: https://developer.allegro.pl/documentation/#/
Schema:
"""
from __future__ import unicode_literals

from ..base import BaseApi
from .saleoffers import SaleOffers
from .salecategories import SaleCategories
from .saleshippingrates import SaleShippingRates
from .saleimages import SaleImages
from .saleofferpublicationcommands import SaleOfferPublicationCommands
from .saleoffervariants import SaleOfferVariants


class Sale(BaseApi):
    """
    Base Endpoint
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(Sale, self).__init__(*args, **kwargs)
        self.endpoint = 'sale'
        self.offers = SaleOffers(self)
        self.categories = SaleCategories(self)
        self.shipping_rates = SaleShippingRates(self)
        self.images = SaleImages(self)
        self.offer_publication_commands = SaleOfferPublicationCommands(self)
        self.offer_variants = SaleOfferVariants(self)

