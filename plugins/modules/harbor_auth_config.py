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
module: harbor_auth_config
author:
  - Rémi REY (!UNKNOWN)
  - Adrien Boulay (!UNKNOWN)
description:
  - Create/update/delete Harbor configurations using Harbor's REST API.
short_description: Create configuration on Harbor
options:
  auth_mode:
    description: Authentication type
    type: str
    choices:
    - db_auth
    - oidc_auth
    default: "db_auth"
  oidc_name:
    description: Name of the configuration
    required: true
    type: str
  oidc_endpoint:
    description: URL of the auth provider
    required: true
    type: str
  oidc_client_id:
    description: OIDC client ID
    required: true
    type: str
  oidc_client_secret:
    description: OIDC client secret
    required: true
    type: str
  oidc_groups_claim:
    description: The name of the Claim whose value is the list of group names
    required: false
    type: str
  oidc_scope:
    description: The scope sent to the OIDC server
    required: false
    type: str
    default: "openid,offline_access"
  oidc_validate_cert:
    description: Weither the OIDC server certificate should be validated or not
    required: false
    type: bool
    default: True
  database_allow_self_registration:
    description: Enable self registration when `auth_mode` is `db_auth`.
    required: false
    type: bool
    default: false
extends_documentation_fragment:
  - sfr.harbor.harbor
'''

EXAMPLES = '''
- name: Enable OpenID authentication
  harbor_auth_config:
    harbor_url: "http://{{ local_harbor }}"
    harbor_username: "{{ harbor_admin_user }}"
    harbor_password: "{{ harbor_admin_password }}"
    auth_mode: oidc_auth
    oidc_name: "keycloak"
    oidc_endpoint: "https://keycloak.example.com/auth/realms/some_realm"
    oidc_client_id: "harbor-instance-0"
    oidc_client_secret: "{{ some_vaulted_secret }}"
    oidc_scope: "openid,email,offline_access,profile"
    oidc_groups_claim: "groups"
    oidc_validate_cert: false

- name: Enable database authentication
  harbor_auth_config:
    harbor_url: "http://{{ local_harbor }}"
    harbor_username: "{{ harbor_admin_user }}"
    harbor_password: "{{ harbor_admin_password }}"
    auth_mode: db_auth
    database_allow_self_registration: true
'''

RETURN = '''
---
configurations:
  description: Configuration structure returned by the Harbor API
  returned: On success
  type: complex
  contains:
    configurations:
        description: The configuration structure returned by the api.
        returned: always
        type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.sfr.harbor.plugins.module_utils.base import harbor_argument_spec
from ansible_collections.sfr.harbor.plugins.module_utils.harbor import HarborBaseInterface

__metaclass__ = type


class HarborInterface(HarborBaseInterface):

    def get_configurations(self):
        url = "/api/configurations"
        response = self._send_request(url, headers=self.headers, method="GET")
        if not response:
            self._module.fail_json(msg="Got no response from server")
        return response

    def update_configurations(self, data):
        url = "/api/configurations"
        self._send_request(url, data=data, headers=self.headers, method="PUT")


def setup_module_object():
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
        required_together=[['harbor_username', 'harbor_password']],
        required_if=[
            ('auth_mode', 'oidc_auth', ["oidc_name", "oidc_endpoint", "oidc_client_id", "oidc_client_secret"]),
        ],
    )
    return module


argument_spec = harbor_argument_spec()

argument_spec.update(
    auth_mode=dict(type='str', default="db_auth", choices=["oidc_auth", "db_auth"]),
    oidc_name=dict(type='str'),
    oidc_endpoint=dict(type='str'),
    oidc_client_id=dict(type='str'),
    oidc_client_secret=dict(type='str', no_log=True),
    oidc_scope=dict(type='str', default="openid,offline_access"),
    oidc_groups_claim=dict(type='str', required=False),
    oidc_validate_cert=dict(type='bool', default=True),
    database_allow_self_registration=dict(type='bool', default=False),
)


def ansible_conf_to_harborconf(data):
    harborconf = {}
    for key, val in data.items():
        harborconf[key] = {"value": val, "editable": False}
    return harborconf


def diff_conf(requested_conf, current_conf):
    diff = {}
    for key, requested_val in requested_conf.items():
        if key in ["oidc_client_secret"]:
            continue
        if current_conf.get(key)["value"] != requested_val.get("value"):
            diff[key] = requested_val
    return diff


def get_oidc_required_conf(module):
    return {
        "auth_mode": module.params['auth_mode'],
        "oidc_name": module.params['oidc_name'],
        "oidc_endpoint": module.params['oidc_endpoint'],
        "oidc_client_id": module.params['oidc_client_id'],
        "oidc_client_secret": module.params['oidc_client_secret'],
        "oidc_scope": module.params['oidc_scope'],
        "oidc_groups_claim": module.params['oidc_groups_claim'],
        "oidc_validate_cert": module.params['oidc_validate_cert']
    }


def get_database_required_conf(module):
    return {
        "auth_mode": module.params['auth_mode'],
        "self_registration": module.params['database_allow_self_registration']
    }


def main():

    module = setup_module_object()
    auth_mode = module.params['auth_mode']

    harbor_iface = HarborInterface(module)
    changed = False

    current_conf = harbor_iface.get_configurations()
    if auth_mode == "oidc_auth":
        requested_conf = get_oidc_required_conf(module)
        if diff_conf(ansible_conf_to_harborconf(requested_conf), current_conf):
            harbor_iface.update_configurations(requested_conf)
            current_conf = harbor_iface.get_configurations()
            changed = True
    elif auth_mode == "db_auth":
        requested_conf = get_database_required_conf(module)
        if diff_conf(ansible_conf_to_harborconf(requested_conf), current_conf):
            harbor_iface.update_configurations(requested_conf)
            current_conf = harbor_iface.get_configurations()
            changed = True
    else:
        module.fail_json(msg="Unsupported auth_mode")
    module.exit_json(changed=changed, configurations=current_conf)


if __name__ == '__main__':
    main()

