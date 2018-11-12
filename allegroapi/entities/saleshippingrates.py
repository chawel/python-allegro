# coding=utf-8
"""
[BETA] The Sale Shipping Rates endpoint

Documentation: https://developer.allegro.pl/documentation/#/
Schema:
"""
from __future__ import unicode_literals

from ..base import BaseApi


class SaleShippingRates(BaseApi):
    """
    Manage shipping rates (cenniki dostaw)
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(SaleShippingRates, self).__init__(*args, **kwargs)
        self.endpoint = 'sale/shipping-rates'
        self.seller_id = None
        self.shipping_rate_id = None

        # Custom header for this endpoint
        self._headers = {'Accept': 'application/vnd.allegro.public.v1+json',
                         'Content-type': 'application/vnd.allegro.public.v1+json'}

    def get(self, shipping_rate_id):
        """
        Get information about specific shipping rate

        :param shipping_rate_id: The unique id (UUID) for the shipping rate.
        :type shipping_rate_id: :py:class:`str`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """

        self.shipping_rate_id = shipping_rate_id
        self.seller_id = None
        return self._a_client._get(url=self._build_path(shipping_rate_id), headers=self._headers)

    def all(self, seller_id):
        """
        Get a list of categories

        :param seller_id: The seller's unique id (UUID).
        :type seller_id: :py:class:`str`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """

        self.seller_id = seller_id
        self.shipping_rate_id = None
        _params = {'seller.id': seller_id}
        # TODO: Maybe iterate or pagination?
        return self._a_client._get(url=self._build_path(), params=_params, headers=self._headers)

