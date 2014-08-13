# -*- coding: utf-8 -*-

import requests

from urllib import urlencode
from requests.auth import HTTPBasicAuth


class Toggl(object):

    def __init__(self, api_token):
        self.api_token = api_token

    def _make_url(self, section='time_entries', params={}):
        url = 'https://www.toggl.com/api/v8/{}'.format(section)
        if len(params) > 0:
            url = url + '?{}'.format(urlencode(params))
        return url

    def _make_get_request(self, url):
        headers = {'content-type': 'application/json'}
        return requests.get(url, headers=headers, auth=HTTPBasicAuth(self.api_token, 'api_token'))

    def _make_post_request(self, url):
        headers = {'content-type': 'application/json'}
        return requests.post(url, headers=headers, auth=HTTPBasicAuth(self.api_token, 'api_token'))

    def get_time_entries(self, start_date='', end_date=''):
        """
        Get Time Entries
        """

        url = self._make_url(section='time_entries', params={'start_date': start_date, 'end_date': end_date})
        r = self._make_get_request(url)
        return r.json()
