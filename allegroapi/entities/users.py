# coding=utf-8
"""
The Users endpoint

Documentation: https://developer.allegro.pl/documentation/#/
Schema:
"""
from __future__ import unicode_literals

from ..base import BaseApi
from .userratingssummary import UserRatingsSummary


class Users(BaseApi):
    """
    Base Endpoint
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(Users, self).__init__(*args, **kwargs)
        self.endpoint = 'users'
        self.ratings_summary = UserRatingsSummary(self)
