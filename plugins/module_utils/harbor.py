# -*- coding: utf-8 -*-
#
# Copyright: (c) 2019, SFR
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import json
from ansible.module_utils.urls import fetch_url, url_argument_spec, basic_auth_header
from ansible.module_utils._text import to_bytes

__metaclass__ = type


class HarborBaseInterface(object):

    def __init__(self, module):
        self._module = module
        # {{{ Authentication header
        self.headers = {"Content-Type": "application/json"}
        self.headers["Authorization"] = basic_auth_header(module.params['harbor_username'], module.params['harbor_password'])
        # }}}
        self.harbor_url = module.params.get("harbor_url")

    def _send_request(self, path, data=None, headers=None, method="GET"):
        if data is not None:
            data = json.dumps(data, sort_keys=True)
        if not headers:
            headers = []
        full_url = "{harbor_url}{path}".format(harbor_url=self.harbor_url, path=path)
        resp, info = fetch_url(self._module, full_url, data=data, headers=headers, method=method)
        status_code = info["status"]
        if status_code == 404:
            if to_bytes("Page Not Found") in info['body']:
                self._module.fail_json(msg="URL %s not found" % full_url, reason="page not found")
            else:
                return None
        elif status_code == 401:
            self._module.fail_json(msg="Unauthorized to perform action '%s' on '%s'" % (method, full_url))
        elif status_code == 403:
            self._module.fail_json(msg="Permission Denied")
        elif 200 <= status_code < 300:
            content = resp.read()
            if content:
                return self._module.from_json(content)
            else:
                return None
        elif status_code == 401:
            self._module.fail_json(msg="Unauthorized to perform action '%s' on '%s'" % (method, full_url))
        elif status_code == 403:
            self._module.fail_json(msg="Permission Denied")
        self._module.fail_json(
            failed=True,
            msg="Harbor API answered with HTTP %d, url %s, response %s, payload %s" % (status_code, full_url, resp, data))
