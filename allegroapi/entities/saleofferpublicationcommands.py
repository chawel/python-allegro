# coding=utf-8
"""
[BETA] The Sale Offer Publication Commands endpoint

Documentation: https://developer.allegro.pl/documentation/#/
Schema:
"""
from __future__ import unicode_literals

from ..base import BaseApi
from .saleofferpublicationcommandtasks import SaleOfferPublicationCommandTasks


class SaleOfferPublicationCommands(BaseApi):
    """
    Manage offer commands
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(SaleOfferPublicationCommands, self).__init__(*args, **kwargs)
        self.endpoint = 'sale/offer-publication-commands'
        self.command_uuid = None
        self.tasks = SaleOfferPublicationCommandTasks(self)

        # Custom header for this endpoint (beta)
        self._headers = {'Accept': 'application/vnd.allegro.beta.v1+json',
                         'Content-type': 'application/vnd.allegro.beta.v1+json'}

    def create(self, command_uuid, body):
        """
        Allows modification of multiple offers' publication at once.

        :param command_uuid: The global unique ID (UUID) for this specific command
        :type command_uuid: :py:class:`str`
        :param body: The request body parameters
        :type body: :py:class:`dict`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """

        self.command_uuid = command_uuid
        if not isinstance(body, dict):
            raise KeyError('The command must have a data')
        return self._a_client._put(url=self._build_path(command_uuid), json=body, headers=self._headers)

    def get(self, command_uuid):
        """
        Provides report summary for given command id

        :param command_uuid: The global unique command ID (UUID)
        :type command_uuid: :py:class:`str`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """

        self.command_uuid = command_uuid
        return self._a_client._get(url=self._build_path(command_uuid), headers=self._headers)

