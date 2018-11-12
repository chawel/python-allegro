# coding=utf-8
"""
[BETA] The Offer Renew Commands endpoint

Documentation: https://developer.allegro.pl/documentation/#/
Schema:
"""
from __future__ import unicode_literals

from ..base import BaseApi


class OfferRenewCommands(BaseApi):
    """
    Manage offer renew commands
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(OfferRenewCommands, self).__init__(*args, **kwargs)
        self.endpoint = 'offers'
        self.command_uuid = None
        self.offer_id = None

        # Custom header for this endpoint
        self._headers = {'Accept': 'application/vnd.allegro.public.v1+json',
                         'Content-type': 'application/vnd.allegro.public.v1+json'}

    def create(self, offer_id, command_uuid, body):
        """
        Renew a single offer by id.

        :param offer_id: The unique id for the offer.
        :type offer_id: :py:class:`str`
        :param command_uuid: The global unique ID (UUID) for this specific command
        :type command_uuid: :py:class:`str`
        :param body: The request's body
        :type body: :py:class:`dict`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """

        self.offer_id = offer_id
        self.command_uuid = command_uuid
        if not isinstance(body, dict):
            raise KeyError('The command must have a data')
        return self._a_client._put(url=self._build_path(offer_id, 'renew-commands', command_uuid),
                                   json=body,
                                   headers=self._headers)

    def get(self, offer_id, command_uuid):
        """
        Provides report summary for given command id

        :param offer_id: The unique id for the offer.
        :type offer_id: :py:class:`str`
        :param command_uuid: The global unique command ID (UUID)
        :type command_uuid: :py:class:`str`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """

        self.offer_id = offer_id
        self.command_uuid = command_uuid
        return self._a_client._get(url=self._build_path(offer_id, 'renew-commands', command_uuid),
                                   headers=self._headers)


