# coding=utf-8
"""
Allegro REST API client

Documentation: https://developer.allegro.pl/about/#rest-api
"""
from __future__ import unicode_literals

import requests
import logging
from .oauth import AllegroAuthHandler
from .error import AllegroError

_logger = logging.getLogger(__name__)

API_URL = 'https://api.allegro.pl'
OAUTH_URL = 'https://allegro.pl/auth/oauth'

SANDBOX_API_URL = 'https://api.allegro.pl.allegrosandbox.pl'
SANDBOX_OAUTH_URL = 'https://allegro.pl.allegrosandbox.pl/auth/oauth'


class AllegroClient(object):
    """
    Core class used to connect and handle basic communication with Allegro.pl REST API
    """
    def __init__(self, client_id, client_secret, api_key, redirect_uri, sandbox=True,
                 timeout=None, request_headers=None, request_hooks=None,
                 access_token=None, refresh_token=None):
        """
        Initialize the class with your client_id, client_secret, api_key, redirect_uri

        If you have `access_token` or / and `refresh_token` provide them as optional arguments
        If you want acquire them for the first time, use `sign_in()` method

        If `sandbox` is True, these client connects to Allegro.pl Sandbox REST API.
        For more info: https://developer.allegro.pl/about/#Sandbox

        :param client_id: Client ID
        :type client_id: :py:class:`str`
        :param client_secret: Client Secret
        :type client_secret: :py:class:`str`
        :param api_key: API Key
        :type api_key: :py:class:`str`
        :param redirect_uri: Redirect URI
        :type redirect_uri: :py:class:`str`
        :param sandbox: Boolean that controls whether we connect to sandbox or production. Default is True (connect to sandbox)
        :type sandbox: :py:class:`bool`
        :param timeout: How many seconds to wait for the server to send data before giving up
        :type timeout: float or tuple
        :param request_headers: Dictionary of HTTP Headers to send with the Request (override defaults)
        :type request_headers: :py:class:`dict`
        :param request_hooks: Request Event-handling hooks
        :type request_hooks: :py:class:`dict`
        :param access_token: Access Token (only valid with correct credentials)
        :type access_token: :py:class:`str`
        :param refresh_token: Refresh Token (provide if you wish to use automatic refresh function)
        :type refresh_token: :py:class:`str`
        """

        # Use super() even for parent class (that inherits from object)
        # more info: http://amyboyle.ninja/Python-Inheritance
        super(AllegroClient, self).__init__()

        # Set URI's for API Client (sandbox or production)
        if sandbox:
            self.base_url = SANDBOX_API_URL
            self.auth_url = SANDBOX_OAUTH_URL
        else:
            self.base_url = API_URL
            self.auth_url = OAUTH_URL

        self.auth_handler = AllegroAuthHandler(client_id, client_secret, api_key,
                                               self.auth_url, redirect_uri,
                                               access_token=access_token,
                                               refresh_token=refresh_token)

        # Get authentication object (session headers)
        self.auth = self.auth_handler.apply_auth()

        self.timeout = timeout
        self.request_hooks = request_hooks

        self.request_headers = self._default_headers

        if isinstance(request_headers, dict):
            self.request_headers.update(request_headers)

    def sign_in(self):
        """
        Handle OAuth2 client authentication flow (register application)
        Using provided credentials and redirect_uri
        Authorizes this instance of `AllegroClient`

        :return: The JSON response from API
        :rtype: :py:class:`dict`
        """
        auth_response = self.auth_handler.fetch_access_token()
        self.auth = self.auth_handler.apply_auth()

        return auth_response

    @property
    def _default_headers(self):
        headers = dict()
        headers['charset'] = 'utf-8'
        headers['Accept-Language'] = 'pl-PL'
        headers['Content-type'] = 'application/json'
        headers['Accept'] = 'application/vnd.allegro.public.v1+json'

        return headers

    def _make_request(self, **kwargs):
        _logger.info(u'{method} Request: {url}'.format(**kwargs))

        # Register how many times tried to resend same request
        _tries = kwargs.pop('tries', 0) + 1

        if kwargs.get('json'):
            _logger.info('PAYLOAD: {json}'.format(**kwargs))

        if kwargs.get('headers'):
            _logger.info('PAYLOAD: {headers}'.format(**kwargs))

        try:
            response = requests.request(**kwargs)

            _logger.info(u'{method} Response: {status} {text}'
                         .format(method=kwargs['method'], status=response.status_code, text=response.text))

        except requests.exceptions.RequestException as e:
            raise e
        else:
            if response.status_code == 401:
                # First check if max tries limit exceeded
                if _tries > 10:
                    raise AllegroError("Could not refresh token! Please check credentials or connection!")

                # Refresh access token...
                _logger.info(u'Response 401: Refreshing token....')
                self.auth_handler.refresh_access_token()
                self.auth = self.auth_handler.apply_auth()

                # ...and resend last request with new auth
                kwargs['auth'] = self.auth
                return self._make_request(tries=_tries, **kwargs)

            if response.status_code >= 400:
                if response.status_code == 404:
                    raise AllegroError("404 Not Found")
                else:
                    raise AllegroError(response.json())

            return response

    def _post(self, url, json=None, headers=None, data=None, files=None):
        """
        Handle authenticated POST requests

        :param url: The url for the endpoint
        :type url: :py:class:`str`
        :param json: The request body to be converted to json
        :type json: :py:data:`none` or :py:class:`dict`
        :param data: The request body data
        :type data: :py:data:`none` or :py:class:`dict`
        :param headers: Update headers with provided in this parameter (for this request only)
        :type headers: :py:data:`none` or :py:class:`dict`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """
        url = requests.compat.urljoin(self.base_url, url)

        # Update headers if necessary
        if isinstance(headers, dict):
            _headers = self.request_headers.copy()
            _headers.update(headers)
        else:
            _headers = self.request_headers

        r = self._make_request(**dict(
            method='POST',
            url=url,
            json=json,
            data=data,
            auth=self.auth,
            timeout=self.timeout,
            hooks=self.request_hooks,
            headers=_headers,
            files=files
        ))

        if r.status_code == 204:
            return None

        return r.json()

    def _get(self, url, params=None, headers=None):
        """
        Handle authenticated GET requests

        :param url: The url for the endpoint
        :type url: :py:class:`str`
        :param params: The query string parameters
        :type params: :py:class:`dict`
        :param headers: Update headers with provided in this parameter (for this request only)
        :type headers: :py:data:`none` or :py:class:`dict`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """
        url = requests.compat.urljoin(self.base_url, url)
        # if len(queryparams):
        #     url += '?' + requests.compat.urlencode(queryparams)

        # Update headers if necessary
        if isinstance(headers, dict):
            _headers = self.request_headers.copy()
            _headers.update(headers)
        else:
            _headers = self.request_headers

        r = self._make_request(**dict(
            method='GET',
            url=url,
            params=params,
            auth=self.auth,
            timeout=self.timeout,
            hooks=self.request_hooks,
            headers=_headers
        ))

        if r.status_code == 204:
            return None

        return r.json()

    def _delete(self, url, headers=None):
        """
        Handle authenticated DELETE requests

        :param url: The url for the endpoint
        :type url: :py:class:`str`
        :param headers: Update headers with provided in this parameter (for this request only)
        :type headers: :py:data:`none` or :py:class:`dict`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """
        url = requests.compat.urljoin(self.base_url, url)

        # Update headers if necessary
        if isinstance(headers, dict):
            _headers = self.request_headers.copy()
            _headers.update(headers)
        else:
            _headers = self.request_headers

        r = self._make_request(**dict(
            method='DELETE',
            url=url,
            auth=self.auth,
            timeout=self.timeout,
            hooks=self.request_hooks,
            headers=_headers
        ))

        if r.status_code == 204:
            return None

        return r.json()

    def _patch(self, url, json=None, headers=None, data=None):
        """
        Handle authenticated PATCH requests

        :param url: The url for the endpoint
        :type url: :py:class:`str`
        :param json: The request body to be converted to json
        :type json: :py:data:`none` or :py:class:`dict`
        :param data: The request body data
        :type data: :py:data:`none` or :py:class:`dict`
        :param headers: Update headers with provided in this parameter (for this request only)
        :type headers: :py:data:`none` or :py:class:`dict`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """
        url = requests.compat.urljoin(self.base_url, url)

        # Update headers if necessary
        if isinstance(headers, dict):
            _headers = self.request_headers.copy()
            _headers.update(headers)
        else:
            _headers = self.request_headers

        r = self._make_request(**dict(
            method='PATCH',
            url=url,
            json=json,
            data=data,
            auth=self.auth,
            timeout=self.timeout,
            hooks=self.request_hooks,
            headers=_headers
        ))

        if r.status_code == 204:
            return None

        return r.json()

    def _put(self, url, json=None, headers=None, data=None):
        """
        Handle authenticated PUT requests

        :param url: The url for the endpoint
        :type url: :py:class:`str`
        :param json: The request body to be converted to json
        :type json: :py:data:`none` or :py:class:`dict`
        :param data: The request body data
        :type data: :py:data:`none` or :py:class:`dict`
        :param headers: Update headers with provided in this parameter (for this request only)
        :type headers: :py:data:`none` or :py:class:`dict`
        :return: The JSON response from API or error or None (if 204)
        :rtype: :py:class:`dict` or :py:data:`none`
        """
        url = requests.compat.urljoin(self.base_url, url)

        # Update headers if necessary
        if isinstance(headers, dict):
            _headers = self.request_headers.copy()
            _headers.update(headers)
        else:
            _headers = self.request_headers

        r = self._make_request(**dict(
            method='PUT',
            url=url,
            json=json,
            data=data,
            auth=self.auth,
            timeout=self.timeout,
            hooks=self.request_hooks,
            headers=_headers
        ))

        if r.status_code == 204:
            return None

        return r.json()
