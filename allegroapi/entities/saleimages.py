# coding=utf-8
"""
[BETA] The Sale Images endpoint

Documentation: https://developer.allegro.pl/documentation/#/
Schema:
"""
from __future__ import unicode_literals

from ..base import BaseApi


class SaleImages(BaseApi):
    """
    Manage offer images
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(SaleImages, self).__init__(*args, **kwargs)
        self.endpoint = 'sale/images'

        # Custom header for this endpoint
        self._headers = {'Accept': 'application/vnd.allegro.public.v1+json',
                         'Content-type': 'image/jpeg'}

    def upload(self, image_location, image_type='JPG'):
        """
        Upload local image
        ex. upload("/imgs/1.jpg", "JPG")

        :param image_location: The location of image file (must not be URL but local!)
        :type image_location: :py:class:`str`
        :param image_type: (JPG, PNG, GIF) Image format for proper headers
        :type image_type: :py:class:`str`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """
        image_format_map = {'JPG': 'image/jpeg',
                            'PNG': 'image/png',
                            'GIF': 'image/gif'}

        self._headers['Content-type'] = image_format_map.get(image_type)

        with open(image_location, 'rb') as f:
            _file_read = f.read()

        return self._a_client._post(url=self._build_path(), data=_file_read, headers=self._headers)

