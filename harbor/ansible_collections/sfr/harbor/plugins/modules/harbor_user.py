#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

ANSIBLE_METADATA = {
    'status': ['preview'],
    'supported_by': 'community',
    'metadata_version': '1.1'
}

DOCUMENTATION = '''
---
module: harbor_user
description:
  - Create/update/delete Harbor users using Harbor's REST API.
options:
  url:
    description:
      - The URL of the target Harbor server's API.
    required: true
    type: str
    aliases: ["harbor_url"]
  url_username:
    description:
      - The username used for basic authentication with Harbor.
    required: true
    type: str
    aliases: ["harbor_user"]
    default: "admin"
  url_password:
    description:
      - The password used for basic authentication with Harbor.
    required: true
    type: str
    aliases: ["harbor_password"]
    default: "Harbor12345"
  username:
    description:
      - The user for API authentication.
    required: true
    type: str
  password:
    description:
      - The user password for API authentication.
    required: true
    type: str
    default: "ChangeMe123"
  email:
    description:
      - The mail address associated with the user.
    required: true
    type: str
  state:
    description:
      - The desired state.
    required: true
    type: str
    choices: ["present", "absent"]
    default: "present"
  use_proxy:
    description:
      - If C(no), it will not use a proxy, even if one is defined in an environment variable on the target hosts.
    type: bool
    default: yes
  client_cert:
    description:
      - PEM formatted certificate chain file to be used for SSL client authentication.
      - This file can also include the key as well, and if the key is included, I(client_key) is not required
    type: path
  client_key:
    description:
      - PEM formatted file that contains your private key to be used for SSL client authentication.
      - If I(client_cert) contains both the certificate and key, this option is not required.
    type: path
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated.
      - This should only set to C(no) used on personally controlled sites using self-signed certificates.
      - Prior to 1.9.2 the code defaulted to C(no).
    type: bool
    default: yes
'''

EXAMPLES = '''
---
- name: create a user
  harbor_user:
      harbor_url: "http://harbor.example.com"
      harbor_user: admin
      harbor_password: Harbor12345
      username: "batman"
      email: "batman@gotham.city"
      state: present

- name: delete a user
  harbor_user:
      harbor_url: "http://harbor.example.com"
      harbor_user: admin
      harbor_password: Harbor12345
      username: "batman"
      email: "batman@gotham.city"
      state: absent
'''

RETURN = '''
---
user:
    description: User information
    returned: On success
    type: complex
    contains:
        email:
            description: The user's email address
            returned: always
            type: str
            sample:
                - "user@example.com"
        user_id:
            description: The user Harbor ID
            returned: always
            type: int
            sample:
                - 42
        username:
            description: The name of the user.
            returned: always
            type: str
            sample:
                - "admin"
'''

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, url_argument_spec, basic_auth_header

__metaclass__ = type


class HarborInterface(object):

    def __init__(self, module):
        self._module = module
        # {{{ Authentication header
        self.headers = {"Content-Type": "application/json", "accept": "application/json"}
        self.headers["Authorization"] = basic_auth_header(module.params['harbor_user'], module.params['harbor_password'])
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
            return None
        elif status_code == 401:
            self._module.fail_json(msg="Unauthorized to perform action '%s' on '%s' header: %s" % (method, full_url, self.headers))
        elif status_code == 403:
            self._module.fail_json(msg="Permission Denied")
        elif 200 <= status_code < 300:
            res = resp.read()
            if res:
                return self._module.from_json(res)
            else:
                return None
        self._module.fail_json(
            msg="Harbor API answered with HTTP %d on %s %s" % (status_code, method, path))

    def create_user(self, username, email, realname, password, comment=None):
        url = "/api/users"
        user = dict(email=email, username=username, realname=realname, password=password, comment=comment)
        response = self._send_request(url, data=user, headers=self.headers, method="POST")
        return response

    def get_user_by_name(self, name):
        url = "/api/users?username={name}".format(name=name)
        response = self._send_request(url, headers=self.headers, method="GET")
        if len(response) == 0:
            return None
        elif len(response) > 1:
            raise Exception("Failed to get user. Expected 1 got %d" % len(response))
        return response[0]

    def delete_user(self, user_id):
        url = "/api/users/{user_id}".format(user_id=user_id)
        response = self._send_request(url, headers=self.headers, method="DELETE")
        return response


def setup_module_object():
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False
    )
    return module


argument_spec = url_argument_spec()
# remove unnecessary arguments
del argument_spec['force']
del argument_spec['force_basic_auth']
del argument_spec['http_agent']

argument_spec.update(
    state=dict(choices=['present', 'absent'], default='present'),
    username=dict(type='str', required=True),
    email=dict(type='str', required=True),
    password=dict(type='str', required=False, default="ChangeMe123", no_log=True),
    url=dict(aliases=["harbor_url"], type='str', required=True),
    url_username=dict(aliases=['harbor_user'], default='admin'),
    url_password=dict(aliases=['harbor_password'], default='Harbor12345', no_log=True),
)


def main():

    module = setup_module_object()
    state = module.params['state']
    username = module.params['username']
    password = module.params['password']
    email = module.params['email']

    # Unimplemented
    realname = username

    harbor_iface = HarborInterface(module)

    changed = False
    if state == 'present':
        user = harbor_iface.get_user_by_name(username)
        if user is None:
            harbor_iface.create_user(username, email, realname, password)
            user = harbor_iface.get_user_by_name(username)
            changed = True
        module.exit_json(changed=changed, user=user)
    elif state == 'absent':
        user = harbor_iface.get_user_by_name(username)
        if user is None:
            module.exit_json(changed=False, message="No user found")
        result = harbor_iface.delete_user(user.get("user_id"))
        module.exit_json(changed=True, message="user deleted")


if __name__ == '__main__':
    main()
