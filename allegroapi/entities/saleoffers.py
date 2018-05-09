# coding=utf-8
"""
[BETA] The Sale Offer endpoint

Documentation: https://developer.allegro.pl/documentation/#/
Schema:
"""
from __future__ import unicode_literals

from ..base import BaseApi


class SaleOffers(BaseApi):
    """
    Manage Offers
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(SaleOffers, self).__init__(*args, **kwargs)
        self.endpoint = 'sale/offers'
        self.offer_id = None

        # Custom header for this endpoint (beta)
        self._headers = {'Accept': 'application/vnd.allegro.beta.v1+json',
                         'Content-type': 'application/vnd.allegro.beta.v1+json'}

    def get(self, offer_id):
        """
        Get information about a single offer from Your Allegro.pl account

        :param offer_id: The unique id for the offer.
        :type offer_id: :py:class:`str`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """

        self.offer_id = offer_id
        return self._a_client._get(url=self._build_path(offer_id), headers=self._headers)

    def update(self, offer_id, data):
        """
        Update a single offer (auction or draft) by id.

        Caution! If updating ongoing offer - you must provide ALL fields in `data` parameter
        (even for single field update!)

        :param offer_id: The unique id for the offer.
        :type offer_id: :py:class:`str`
        :param data: The request's body (when updating ongoing offer - provide whole structure of the offer)
        :type data: :py:class:`dict`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """

        self.offer_id = offer_id
        if not isinstance(data, dict):
            raise KeyError('The offer must have a data')
        return self._a_client._put(url=self._build_path(offer_id), data=data, headers=self._headers)

    def create(self, data):
        """
        Create a new offer or draft.

        :param data: The request body parameters
        :type data: :py:class:`dict`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """
        if 'name' not in data:
            raise KeyError('The offer must have a name')
        if 'category' not in data:
            raise KeyError('The offer must have category')
        if 'id' not in data['category']:
            raise KeyError('The offer must have category id')
        if 'publication' not in data:
            raise KeyError('The offer must have publication information')
        if 'status' not in data['publication']:
            raise KeyError('The offer must have status INACTIVE (for draft) or ACTIVE (for offer)')

        response = self._a_client._post(url=self._build_path(), data=data, headers=self._headers)
        if response is not None:
            self.offer_id = response['id']
        else:
            self.offer_id = None
        return response

