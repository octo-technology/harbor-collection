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
module: harbor.users

description:
  - Create/update/delete Harbor users using Harbor's REST API.
options:
  harbor_url:
    description:
      - The URL of the target Harbor server's API.
    required: true
    type: str
  email:
    description:
      - The mail address associated with the user.
    required: true
    type: str
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
'''

EXAMPLES = '''
---
- name: Create a user with default password 'ChangeMe123'
  harbor_user:
      url: "https://harbor.example.com"
      username: "adminuser"
      email: "adminuser@example.com"
      state: present
- name: Create a user with specified password
  harbor_user:
      url: "https://harbor.example.com"
      username: "adminuser"
      password: "specified password"
      email: "adminuser@example.com"
      state: present
- name: Delete a user
  harbor_user:
      url: "https://harbor.example.com"
      name: "adminuser"
      email: "adminuser@example.com"
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
            return None
        elif status_code == 401:
            self._module.fail_json(failed=True, msg="Unauthorized to perform action '%s' on '%s' header: %s" % (method, full_url, self.headers))
        elif status_code == 403:
            self._module.fail_json(failed=True, msg="Permission Denied")
        elif status_code == 200:
            return self._module.from_json(resp.read())
        self._module.fail_json(failed=True, msg="Harbor API answered with HTTP %d" % status_code)

    def create_user(self, name, email, realname, password="ChangeMe123"):
        url = "/api/users"
        user = dict(email=email, username=name, realname=realname if name else name, password=password, comment=None)
        response = self._send_request(url, data=user, headers=self.headers, method="POST")
        return response

    def get_user_by_name(self, name):
        url = "/api/users?username={name}".format(name=name)
        response = self._send_request(url, headers=self.headers, method="GET")
        if not len(response) == 1:
            raise AssertionError("Expected 1 user, got %d" % len(response))

        if len(response) == 0:
            return None
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
    name=dict(type='str', required=True),
    email=dict(type='str', required=True),
    password=dict(type='list', required=False),
    harbor_url=dict(type='str', required=True),
    harbor_username=dict(aliases=['harbor_user'], default='admin'),
    harbor_password=dict(aliases=['harbor_password'], default='admin', no_log=True),
)


def main():

    module = setup_module_object()
    state = module.params['state']
    name = module.params['name']
    email = module.params['email']

    harbor_iface = HarborInterface(module)

    changed = False
    if state == 'present':
        user = harbor_iface.get_user_by_name(name)
        if user is None:
            harbor_iface.create_user(name, email, realname=name)
            user = harbor_iface.get_user_by_name(name)
            changed = True
        module.exit_json(failed=False, changed=changed, user=user)
    elif state == 'absent':
        user = harbor_iface.get_user_by_name(name)
        if user is None:
            module.exit_json(failed=False, changed=False, message="No team found")
        result = harbor_iface.delete_user(user.get("user_id"))
        module.exit_json(failed=False, changed=True, message=result.get("message"))


if __name__ == '__main__':
    main()