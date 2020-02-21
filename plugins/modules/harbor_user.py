#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2019, SFR
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

ANSIBLE_METADATA = {
    'status': ['preview'],
    'supported_by': 'community',
    'metadata_version': '1.1'
}

DOCUMENTATION = '''
---
module: harbor_user
author:
  - Antoine Gaudelas (!UNKNOWN)
description:
  - Create/update/delete Harbor users using Harbor's REST API.
short_description: Create user on Harbor
options:
  username:
    description:
      - The user for API authentication.
    required: true
    type: str
  password:
    description:
      - The user password for API authentication.
    required: False
    type: str
    default: "ChangeMe123"
  email:
    description:
      - The mail address associated with the user.
    required: true
    type: str
extends_documentation_fragment:
  - octo.harbor.harbor
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

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.octo.harbor.plugins.module_utils.base import harbor_argument_spec
from ansible_collections.octo.harbor.plugins.module_utils.harbor import HarborBaseInterface

__metaclass__ = type


class HarborInterface(HarborBaseInterface):

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


argument_spec = harbor_argument_spec()

argument_spec.update(
    username=dict(type='str', required=True),
    email=dict(type='str', required=True),
    password=dict(type='str', required=False, default="ChangeMe123", no_log=True)
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
