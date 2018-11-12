# coding=utf-8
"""
[BETA] The Sale Category Parameters endpoint

Documentation: https://developer.allegro.pl/documentation/#/
Schema:
"""
from __future__ import unicode_literals

from ..base import BaseApi


class SaleCategoryParameters(BaseApi):
    """
    Manage category parameters
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(SaleCategoryParameters, self).__init__(*args, **kwargs)
        self.endpoint = 'sale/categories'
        self.category_id = None

        # Custom header for this endpoint
        self._headers = {'Accept': 'application/vnd.allegro.public.v1+json',
                         'Content-type': 'application/vnd.allegro.public.v1+json'}

    def get(self, category_id):
        """
        Get parameters of specific category

        :param category_id: The unique id (UUID) for the category.
        :type category_id: :py:class:`str`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """

        self.category_id = category_id
        return self._a_client._get(url=self._build_path(category_id, 'parameters'), headers=self._headers)
