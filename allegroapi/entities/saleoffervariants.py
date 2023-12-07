# coding=utf-8
"""
[BETA] The Sale Offer Variants endpoint

Documentation: https://developer.allegro.pl/documentation/#/
Schema:
"""
from __future__ import unicode_literals

from ..base import BaseApi


class SaleOfferVariants(BaseApi):
    """
    Manage offer variants (aukcje wielowariantowe)
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(SaleOfferVariants, self).__init__(*args, **kwargs)
        self.endpoint = 'sale/offer-variants'
        self.set_id = None

        # Custom header for this endpoint
        self._headers = {'Accept': 'application/vnd.allegro.public.v1+json',
                         'Content-type': 'application/vnd.allegro.public.v1+json'}

    def get(self, set_id):
        """
        Use this resource to get variant set by set id.

        :param set_id: The unique id (UUID) for the variant set
        :type set_id: :py:class:`str`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """

        self.set_id = set_id
        return self._a_client._get(url=self._build_path(set_id), headers=self._headers)

    def _list_request(self, limit=50, offset=0):
        """
        Single request to list up to 50 variant sets.
        :param limit: Limit the number of offers in one response
        :type limit: :py:class:`int`
        :return: the JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """
        return self._a_client._get(url=self._build_path(limit=limit, offset=offset), headers=self._headers)

    def list(self, quantity: int=False):
        """
        Use this resource to get variant sets available for your Allegro account.
        :param quantity: Quantity limit of variant sets to be returned
        :type quantity: :py:class:`int`
        :return: the JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """
        limit = 50
        initial_limit = 50
        need_one_request = False

        if quantity is not False:
            if quantity < 10:
                raise ValueError('quantity must be greater than 10')
            if quantity < limit:
                initial_limit = quantity
                need_one_request = True

        initial_response = self._list_request(initial_limit)

        if need_one_request:
            return initial_response

        response_variant_sets_count = initial_response['count']

        if quantity == 0:
            requests_count = response_variant_sets_count // limit
            last_request_limit = response_variant_sets_count % limit
        else:
            requests_count = quantity // limit
            last_request_limit = quantity % limit

        for i in range(1, requests_count+1):
            offset = i*limit
            if i == requests_count:
                limit = last_request_limit
            response = self._list_request(limit=limit, offset=offset)
            initial_response['offerVariants'] += response['offerVariants']

        return initial_response

    def create(self, set_id, body):
        """
        Use this resource to create or update variant set.

        :param set_id: The global unique ID (UUID) for this specific command
        :type set_id: :py:class:`str`
        :param body: The request body parameters
        :type body: :py:class:`dict`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`

        A valid variant set must consist of three required elements:

        name: it can't be blank and must not be longer than 50 characters

        parameters: it should contain parameter identifiers used for offer grouping
        parameter identifiers from the offers and special color/pattern value (for grouping via image) are permitted
        it must contain at least one element (up to 2)

        offers: it must contain at least 2 offers (500 at most)

        colorPattern value must be set for every offer if color/pattern parameter is used
        colorPattern value can't be blank and must not be longer than 50 characters
        colorPattern can take arbitrary string value like red, b323592c-522f-4ec1-b9ea-3764538e0ac4 (UUID), etc.
        offers having the same image should have identical colorPattern value
        """

        self.set_id = set_id
        if not isinstance(body, dict):
            raise KeyError('The command must have a data')
        return self._a_client._put(url=self._build_path(set_id), json=body, headers=self._headers)

    def delete(self, set_id):
        """
        Use this resource to delete variant set by id.
        Offers included in variant set will not be stopped or modified by this operation.

        :param set_id: The unique id (UUID) for the variant set
        :type set_id: :py:class:`str`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """

        self.set_id = set_id
        if not set_id:
            raise KeyError('Variant set ID not specified!')
        return self._a_client._delete(url=self._build_path(set_id), headers=self._headers)

