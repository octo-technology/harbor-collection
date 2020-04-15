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
module: harbor_project_members
author:
  - Adrien Boulay (!UNKNOWN)
description:
  - Create/update/delete Harbor projects members using Harbor's REST API.
short_description: Create members on a specific project in Harbor
options:
  project_name:
    description: name of the project
    required: true
    type: str
  members:
    description: members of the projects
    required: true
    type: list
extends_documentation_fragment:
  - octo.harbor.harbor
'''

EXAMPLES = '''

- name: add members to a projects
  harbor_project_members:
    harbor_url: "{{ harbor_url }}"
    harbor_username: "{{ harbor_admin_user }}"
    harbor_password: "{{ harbor_admin_password }}"
    project_name: test_project
    members:
      - type: Group
        name: group_name
        role: admin
      - type: User
        name: user_name
        role: admin

'''

RETURN = '''
---
'''

import itertools
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.octo.harbor.plugins.module_utils.base import harbor_argument_spec
from ansible_collections.octo.harbor.plugins.module_utils.harbor import HarborBaseInterface

__metaclass__ = type


class HarborInterface(HarborBaseInterface):
    def get_project_by_name(self, name):
        url = "/api/projects?name={name}".format(name=name)
        response = self._send_request(url, headers=self.headers, method="GET")
        if not response:
            return None
        if not len(response) == 1:
            raise AssertionError("Expected 1 project, got %d" % len(response))
        project = response[0]
        project_id = project['project_id']
        project['members'] = self.get_project_members(project_id)
        return project

    def get_project_members(self, project_id):
        url = "/api/projects/{project_id}/members".format(project_id=project_id)
        response = self._send_request(url, headers=self.headers, method="GET")
        return response

    def create_project_member(self, project_id, member):
        url = "/api/projects/{project_id}/members".format(project_id=project_id)
        payload = dict(role_id=harbor_roles_equivalence(member["role"]), member_user=dict(username=member["name"]))
        response = self._send_request(url, data=payload, headers=self.headers, method="POST")
        return response

    def update_project_member(self, project_id, member_id, member_updated):
        url = "/api/projects/{project_id}/members/{member_id}".format(project_id=project_id, member_id=member_id)
        payload = dict(role_id=harbor_roles_equivalence(member_updated["role"]))
        response = self._send_request(url, data=payload, headers=self.headers, method="PUT")
        return response

    def delete_project_member(self, project_id, member_id):
        url = "/api/projects/{project_id}/members/{member_id}".format(project_id=project_id, member_id=member_id)
        response = self._send_request(url, headers=self.headers, method="DELETE")
        return response


def setup_module_object():
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
        required_together=[['harbor_username', 'harbor_password']]
    )
    return module


argument_spec = harbor_argument_spec()

argument_spec.update(
    project_name=dict(type='str', required=True),
    members=dict(type='list', defaults=[]),
)


def harbor_roles_equivalence(role_name):
    if role_name == "projectAdmin":
        return 1
    elif role_name == "developer":
        return 2
    elif role_name == "guest":
        return 3
    elif role_name == "master":
        return 4
    else:
        return 99


def convert_harbor_members_dict_to_ansible(harbor_members):
    existing_members = []
    for harbor_member in harbor_members:
        existing_members.append({
            "name": harbor_member["entity_name"],
            "id": harbor_member["id"],
            "type": ("Group" if harbor_member["entity_type"] == "g" else "User"),
            "role": harbor_member["role_name"]
        })
    return existing_members


def main():
    module = setup_module_object()
    name = module.params['project_name']
    members = module.params['members']

    changed = False
    created = False

    harbor_iface = HarborInterface(module)

    project = harbor_iface.get_project_by_name(name)
    project_id = harbor_iface.get_project_by_name(name)["project_id"]

    if project is None:
        module.exit_json(failed=True, changed=False, message="No project found")

    existing_members = harbor_iface.get_project_members(project_id)
    existing_members = convert_harbor_members_dict_to_ansible(existing_members)
    admin_json = [emember for emember in existing_members if (emember["name"] == "admin" and emember["type"] == "User")]
    existing_members.remove(admin_json[0])

    for member in members:
        matches = [emember for emember in existing_members if (emember["name"] == member["name"] and emember["type"] == member["type"])]
        if len(matches) == 0:
            harbor_iface.create_project_member(project_id, member)
            created = True
            changed = True
            continue
        existing_member = matches[0]
        if member["role"] != existing_member["role"]:
            harbor_iface.update_project_member(project_id, existing_member["id"], member)
            changed = True
        existing_members.remove(existing_member)

    for existing_member in existing_members:
        harbor_iface.delete_project_member(project_id, existing_member["id"])
        changed = True

    members_list = harbor_iface.get_project_members(project_id)
    members_list = convert_harbor_members_dict_to_ansible(members_list)

    module.exit_json(failed=False, changed=changed, members=members_list, created=created)


if __name__ == '__main__':
    main()
