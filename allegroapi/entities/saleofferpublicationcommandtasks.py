# coding=utf-8#346 Podpinam się pod ten temat, bo podobny.
"""
[BETA] The Sale Offer Publication Command Tasks endpoint

Documentation: https://developer.allegro.pl/documentation/#/
Schema:
"""
from __future__ import unicode_literals

from ..base import BaseApi


class SaleOfferPublicationCommandTasks(BaseApi):
    """
    Manage publication offer tasks
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(SaleOfferPublicationCommandTasks, self).__init__(*args, **kwargs)
        self.endpoint = 'sale/offer-publication-commands'
        self.command_uuid = None

        # Custom header for this endpoint
        self._headers = {'Accept': 'application/vnd.allegro.public.v1+json',
                         'Content-type': 'application/vnd.allegro.public.v1+json'}

    def get(self, command_uuid, limit=100, offset=0):
        """
        [BETA] Provides detailed report for single command task

        :param command_uuid: The global unique command ID (UUID)
        :type command_uuid: :py:class:`str`
        :param limit: Limit for page
        :type limit: :py:class:`int`
        :param offset: Offset position
        :type offset: :py:class:`int`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """

        self.command_uuid = command_uuid
        _params = {'limit': limit, 'offset': offset}
        return self._a_client._get(url=self._build_path(command_uuid, 'tasks'), params=_params, headers=self._headers)

