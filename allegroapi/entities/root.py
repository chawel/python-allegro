# coding=utf-8
"""
The API Root endpoint

Documentation: https://developer.allegro.pl/documentation/#/
Schema:
"""
from __future__ import unicode_literals

from ..base import BaseApi


class Root(BaseApi):
    """
    The API root resource links to all other resources available in the API.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(Root, self).__init__(*args, **kwargs)
        self.endpoint = ''

    def get(self, **queryparams):
        """
        Get links to all other resources available in the API.

        :param queryparams: The query string parameters
        """
        return self._a_client._get(url=self._build_path(), **queryparams)
