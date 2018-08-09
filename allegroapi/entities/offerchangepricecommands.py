# coding=utf-8
"""
The Offer Change Price Commands endpoint

Documentation: https://developer.allegro.pl/documentation/#/
Schema:
"""
from __future__ import unicode_literals

from ..base import BaseApi


class OfferChangePriceCommands(BaseApi):
    """
    Manage offer price change commands
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(OfferChangePriceCommands, self).__init__(*args, **kwargs)
        self.endpoint = 'offers'
        self.command_uuid = None
        self.offer_id = None

        # Custom header for this endpoint (beta)
        self._headers = {'Accept': 'application/vnd.allegro.public.v1+json',
                         'Content-type': 'application/vnd.allegro.public.v1+json'}

    def create(self, offer_id, command_uuid, body):
        """
        Use it to change a Buy Now price in a single offer

        :param command_uuid: The global unique ID (UUID) for this specific command
        :type command_uuid: :py:class:`str`
        :param offer_id: The unique id for the offer.
        :type offer_id: :py:class:`str`
        :param body: The request's body, Command input data.
            Note that the amount field must be transferred as a string to avoid rounding errors.
            A currency must be provided as a 3-letter code as defined in ISO 4217.
            (https://en.wikipedia.org/wiki/ISO_4217#Active_codes)
        :type body: :py:class:`dict`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """

        self.offer_id = offer_id
        self.command_uuid = command_uuid
        if not isinstance(body, dict):
            raise KeyError('The command must have a data')
        return self._a_client._put(url=self._build_path(offer_id, 'change-price-commands'), json=body, headers=self._headers)

    # def get(self, command_uuid):
    #     pass

