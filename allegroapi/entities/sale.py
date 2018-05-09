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
