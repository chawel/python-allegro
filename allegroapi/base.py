# coding=utf-8
"""
The base API object that allows constructions of various endpoint paths
"""
from __future__ import unicode_literals
from itertools import chain


class BaseApi(object):
    """
    Simple class to buid path for entities
    """

    def __init__(self, a_client):
        """
        Initialize the class with you user_id and secret_key

        :param a_client: Allegro.pl client
        :type a_client: :mod:`allegroapi.allegroclient.AllegroClient`
        """
        super(BaseApi, self).__init__()
        self._a_client = a_client
        self.endpoint = ''

    def _build_path(self, *args, **kwargs):
        """
        Build path with endpoint and args

        :param args: Path elements in the endpoint URL
        :type args: :py:class:`unicode`
        """
        path = '/'.join(chain((self.endpoint,), map(str, args)))
        if kwargs:
            params_path = "&".join(f"{key}={value}" for key, value in kwargs.items())
            path = path + "?" + params_path
            print(path)

        return path
