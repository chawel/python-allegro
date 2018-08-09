from __future__ import unicode_literals

import requests
from requests.auth import HTTPBasicAuth
import webbrowser

# Handle library reorganisation Python 2 > Python 3.
try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from .error import AllegroError


class OAuth2Bearer(requests.auth.AuthBase):
    """
    Authentication class for storing access token and api key
    """
    def __init__(self, api_key, access_token):
        """
        Initialize the OAuth and save the access token

        :param api_key: Api Key
        :type api_key: :py:class:`str`
        :param access_token: The access token provided by OAuth authentication
        :type access_token: :py:class:`str`
        """
        self._api_key = api_key
        self._access_token = access_token

    def __call__(self, r):
        """
        Authorize with the access token and api_key provided in __init__
        """
        # r.headers['Api-Key'] = self._api_key
        r.headers['Authorization'] = "Bearer {}".format(self._access_token)

        return r


class HTTPServerHandler(BaseHTTPRequestHandler):
    """
    HTTP Server callbacks to handle OAuth redirects
    """

    def __init__(self, request, address, server):
        # For Python 3.x you can use just super().__init__(...)
        super(HTTPServerHandler, self).__init__(request, address, server)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if 'code' in self.path:
            self.server.access_code = self.path.rsplit('?code=', 1)[-1]
            # Display to the user that they no longer need the browser window
            self.wfile.write(bytes('<html><h1>You may now close this window.'
                                   + '</h1></html>', 'utf-8'))


class AllegroAuthHandler(object):
    """
    Class used to handle OAuth2 flow
    Documentation: https://developer.allegro.pl/auth/
    """

    def __init__(self, client_id, client_secret, api_auth_url, redirect_uri, api_key=None,
                 access_token=None, refresh_token=None, token_expires_in=None):
        """
        Initialize the class with required client_id, api_key, api_auth_url and redirect_uri.

        :param client_id: Client_id
        :type client_id: :py:class:`str`
        :param client_secret: Client_secret
        :type client_secret: :py:class:`str`
        :param api_key: Api_key (deprecated - not used)
        :type api_key: :py:class:`str`
        :param api_auth_url: URL to Allegro REST API Auth endpoint
        :type api_auth_url: :py:class:`str`
        :param redirect_uri: Redirect URI (ex. "http://localhost:8000/")
        :type redirect_uri: :py:class:`str`
        """
        self._id = client_id
        self._secret = client_secret
        self._api_key = api_key
        # Remove suffix if necessary
        self._auth_url = api_auth_url[:-1] if api_auth_url.endswith('/') else api_auth_url
        self._redirect_uri = redirect_uri

        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expires_in = token_expires_in

    def get_oauth_url(self):
        """
        Returns authentication (OAuth 2) URI generated using provided parameters
        :return: URI for authentication
        :rtype: :py:class:`str`
        """
        base_url = """{auth_url}/authorize?response_type=code&client_id={client_id}&api-key={api_key}&redirect_uri={redirect_uri}"""

        # Just in case requote to ensure correct url format
        return requests.utils.requote_uri(base_url.format(auth_url=self._auth_url,
                                                          client_id=self._id,
                                                          redirect_uri=self._redirect_uri))

    def fetch_oauth_code(self):
        """
        Authorize application with use of graphical web browser, returns authorization code
        :return: Authorization Code
        :rtype: :py:class:`str`
        """
        _parsed_redirect_uri = requests.utils.urlparse(self._redirect_uri)
        _server_address = _parsed_redirect_uri.hostname, _parsed_redirect_uri.port
        _auth_url = self.get_oauth_url()

        httpd = HTTPServer(_server_address, HTTPServerHandler)

        # Open prepared auth url in default web browser
        webbrowser.open(_auth_url)

        # Listen for redirected request
        httpd.handle_request()

        # Then close our local http server
        httpd.server_close()

        # Extract injected access_token variable from HTTPServer class
        auth_code = httpd.access_code

        return auth_code

    def fetch_access_token(self, code=None):
        """
        Requests access token with provided optional authorization code (if not provided, runs get_oauth_code() method)
        :param code: Authorization Code
        :type code: :py:data:`none` or :py:class:`str`
        :return: Dictionary with Access Token, Refresh Token, Expiration Time
        :rtype: :py:class:`dict`
        """
        access_code = self.fetch_oauth_code() if code is None else code

        _url = self._auth_url + '/token'

        access_token_data = {'grant_type': 'authorization_code',
                             'code': access_code,
                             'redirect_uri': self._redirect_uri
                             }

        try:
            r = requests.post(url=_url,
                              auth=HTTPBasicAuth(self._id, self._secret),
                              data=access_token_data)
        except requests.exceptions.RequestException as e:
            raise e
        else:
            if r.status_code >= 400:
                raise AllegroError(r.json())

            response = r.json()
            self.access_token = response['access_token']
            self.refresh_token = response['refresh_token']
            self.token_expires_in = response['expires_in']

            return response

    def refresh_access_token(self, refresh_token=None):
        """
        Gets new access token using provided refresh_token
        :param refresh_token: Refresh Token
        :type refresh_token: :py:class:`str`
        :return: Dictionary with Access Token, Refresh Token, Expiration Time
        :rtype: :py:class:`dict`
        """

        _refresh_token = self.refresh_token if refresh_token is None else refresh_token

        _url = self._auth_url + '/token'

        refresh_token_data = {'grant_type': 'refresh_token',
                              'refresh_token': _refresh_token,
                              'redirect_uri': self._redirect_uri
                              }

        try:
            r = requests.post(url=_url,
                              auth=HTTPBasicAuth(self._id, self._secret),
                              data=refresh_token_data)
        except requests.exceptions.RequestException as e:
            raise e
        else:
            if r.status_code >= 400:
                raise AllegroError(r.json())

            response = r.json()
            self.access_token = response['access_token']
            self.refresh_token = response['refresh_token']
            self.token_expires_in = response['expires_in']

            return response

    def apply_auth(self):
        return OAuth2Bearer(self._api_key, self.access_token)
