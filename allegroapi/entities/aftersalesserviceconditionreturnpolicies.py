# coding=utf-8
"""
[BETA] The After Sale Service Condition Return Policies endpoint

Documentation: https://developer.allegro.pl/documentation/#/
Schema:
"""
from __future__ import unicode_literals

from ..base import BaseApi


class AfterSaleServiceConditionReturnPolicies(BaseApi):
    """
    Manage category tree
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(AfterSaleServiceConditionReturnPolicies, self).__init__(*args, **kwargs)
        self.endpoint = '/after-sales-service-conditions/return-policies'
        self.seller_id = None

        # Custom header for this endpoint
        self._headers = {'Accept': 'application/vnd.allegro.public.v1+json',
                         'Content-type': 'application/vnd.allegro.public.v1+json'}

    def all(self, seller_id=None):
        """
        Get a list of categories

        :param seller_id: The seller's unique id.
        :type seller_id: :py:class:`str`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """

        self.seller_id = seller_id
        _params = {'sellerId': seller_id}
        # TODO: Maybe iterate or pagination?
        return self._a_client._get(url=self._build_path(), params=_params, headers=self._headers)

