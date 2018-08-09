# coding=utf-8
"""
[BETA] The Sale Category endpoint

Documentation: https://developer.allegro.pl/documentation/#/
Schema:
"""
from __future__ import unicode_literals

from ..base import BaseApi
from .salecategoryparameters import SaleCategoryParameters


class SaleCategories(BaseApi):
    """
    Manage category tree
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(SaleCategories, self).__init__(*args, **kwargs)
        self.endpoint = 'sale/categories'
        self.parent_id = None
        self.category_id = None
        self.parameters = SaleCategoryParameters(self)

        # Custom header for this endpoint (beta)
        self._headers = {'Accept': 'application/vnd.allegro.beta.v1+json',
                         'Content-type': 'application/vnd.allegro.beta.v1+json'}

    def get(self, category_id):
        """
        Get information about specific category

        :param category_id: The unique id (UUID) for the category.
        :type category_id: :py:class:`str`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """

        self.category_id = category_id
        self.parent_id = None
        return self._a_client._get(url=self._build_path(category_id), headers=self._headers)

    def all(self, parent_id=None, limit=100, offset=0):
        """
        Get a list of categories

        :param parent_id: The unique id (UUID) for the parent category.
        :type parent_id: :py:class:`str`
        :param limit: Limit for page
        :type limit: :py:class:`int`
        :param offset: Offset position
        :type offset: :py:class:`int`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """

        self.parent_id = parent_id
        self.category_id = None
        _params = {'parent.id': parent_id, 'limit': limit, 'offset': offset}
        # TODO: Maybe iterate or pagination?
        return self._a_client._get(url=self._build_path(), params=_params, headers=self._headers)

