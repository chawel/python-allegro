# coding=utf-8
"""
The User Ratings-Summary endpoint

Documentation: https://developer.allegro.pl/documentation/#/
Schema:
"""
from __future__ import unicode_literals

from ..base import BaseApi


class UserRatingsSummary(BaseApi):
    """
    Get user ratings-summary
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(UserRatingsSummary, self).__init__(*args, **kwargs)
        self.endpoint = 'users'
        self.user_id = None

    def get(self, user_id):
        """
        Get information about specific user's ratings summary

        :param user_id: The user's id
        :type user_id: :py:class:`str`
        """
        self.user_id = user_id
        return self._a_client._get(url=self._build_path(user_id, 'ratings-summary'))
