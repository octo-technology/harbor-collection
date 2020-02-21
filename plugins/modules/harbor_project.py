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
module: harbor_project
author:
  - Antoine Gaudelas (!UNKNOWN)
description:
  - Create/update/delete Harbor projects using Harbor's REST API.
short_description: Create project on Harbor
options:
  name:
    description: name of the project
    required: true
    type: str
  administrators:
    description: list of user names that can administer the project
    required: false
    type: list
  auto_scan:
    description: whether to activate scan-on-push on images or the project
    required: false
    type: bool
    default: false
  quota_disk_space:
    description: the maximum space (in bytes) that the project can use. (-1 means unlimited)
    required: false
    default: -1
    type: int
  quota_artifact_count:
    description: the maximum number of artifacts that can be created in the project (-1 means unlimited)
    required: false
    default: -1
    type: int
extends_documentation_fragment:
  - octo.harbor.harbor
'''

EXAMPLES = '''
- name: create new project
  harbor_project:
    harbor_url: "http://{{ local_harbor }}"
    harbor_username: "{{ harbor_admin_user }}"
    harbor_password: "{{ harbor_admin_password }}"
    name: test_project
    state: present

- name: delete project
  harbor_project:
    harbor_url: "http://{{ local_harbor }}"
    harbor_username: "{{ harbor_admin_user }}"
    harbor_password: "{{ harbor_admin_password }}"
    name: test_project
    state: absent

- name: renable scan-on-push
  harbor_project:
    harbor_url: "http://{{ local_harbor }}"
    harbor_username: "{{ harbor_admin_user }}"
    harbor_password: "{{ harbor_admin_password }}"
    auto_scan: true
    name: test_project
    state: present

- name: add an administrator to a project
  harbor_project:
    harbor_url: "http://{{ local_harbor }}"
    harbor_username: "{{ harbor_admin_user }}"
    harbor_password: "{{ harbor_admin_password }}"
    administrators:
      - test_admin
    name: test_project
    state: present

- name: set maximum disk usage to 10ko and maximum number of images to 12
  harbor_project:
    harbor_url: "http://{{ local_harbor }}"
    harbor_username: "{{ harbor_admin_user }}"
    harbor_password: "{{ harbor_admin_password }}"
    name: test_project
    quota_disk_space: 10240
    quota_artifact_count: 12
    state: present
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

    def create_project(self, name, quota_disk_space, quota_artifact_count):
        url = "/api/projects"
        project = dict(project_name=name, metadata=dict(public="false"), storage_limit=quota_disk_space, count_limit=quota_artifact_count)
        response = self._send_request(url, data=project, headers=self.headers, method="POST")
        return response

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
        project['metadata'] = self.get_project_metadata(project_id)
        retention = self.get_project_retention(project_id)
        if retention:
            project['retention'] = retention
        project['quota'] = self._get_quota_by_project_name(name)
        return project

    def delete_project(self, project_id):
        url = "/api/projects/{project_id}".format(project_id=project_id)
        response = self._send_request(url, headers=self.headers, method="DELETE")
        return response

    def get_project_members(self, project_id):
        url = "/api/projects/{project_id}/members".format(project_id=project_id)
        response = self._send_request(url, headers=self.headers, method="GET")
        return response

    def add_admin_member_to_project(self, user_name, project_id):
        payload = dict(role_id=1, member_user=dict(username=user_name))
        url = "/api/projects/{project_id}/members".format(project_id=project_id)
        response = self._send_request(url, data=payload, headers=self.headers, method="POST")
        return response

    def enable_autoscan(self, project_id, enabled):
        url = "/api/projects/{project_id}".format(project_id=project_id)
        payload = {"metadata": {"auto_scan": "true" if enabled else "false"}}
        response = self._send_request(url, data=payload, headers=self.headers, method="PUT")
        return response

    def _get_quota_by_project_name(self, project_name):
        def get_page(number):
            url = "/api/quotas?page_size=2&page={0}".format(number)
            response = self._send_request(url, headers=self.headers, method="GET")
            if response is None:
                response = []
            for quota in response:
                yield quota

        def get_all():
            for p in itertools.count(start=1):
                page = get_page(p)
                if not page:
                    break
                for quota in page:
                    yield quota

        for quota in get_all():
            if quota['ref']['name'] == project_name:
                return quota

    def update_quota(self, project_name, quota_disk_space, quota_artifact_count):
        quota = self._get_quota_by_project_name(project_name)
        url = "/api/quotas/{quota_id}".format(quota_id=quota["id"])
        payload = {"hard": {"count": quota_artifact_count, "storage": quota_disk_space}}
        response = self._send_request(url, data=payload, headers=self.headers, method="PUT")
        return response

    def get_retention_definition(self, project_id, number_of_images_to_retain):
        rules = [] if number_of_images_to_retain is None else [
            {
                "disabled": False,
                "action": "retain",
                "params": {"latestPushedK": number_of_images_to_retain},
                "scope_selectors": {
                    "repository": [
                        {
                            "kind": "doublestar",
                            "decoration": "repoMatches",
                            "pattern": "**"
                        }
                    ]
                },
                "tag_selectors": [
                    {
                        "kind": "doublestar",
                        "decoration": "matches",
                        "pattern": "*.*.*"
                    }
                ],
                "template": "latestPushedK"
            }
        ]
        payload = {
            "rules": rules,
            "algorithm": "or",
            "trigger": {
                "kind": "Schedule",
                "references": {},
                "settings": {"cron": ""}
            },
            "scope": {"level": "project", "ref": project_id}
        }
        return payload

    def apply_retention_to_project(self, project_id, number_of_images_to_retain, existing_retention):
        payload = self.get_retention_definition(project_id, number_of_images_to_retain)
        retention_id = None if existing_retention is None else existing_retention["id"]
        url = "/api/retentions" if existing_retention is None else "/api/retentions/{id}".format(id=retention_id)
        method = "POST" if existing_retention is None else "PUT"
        response = self._send_request(url, data=payload, headers=self.headers, method=method)
        return response

    def get_project_retention(self, project_id):
        retention_id = self.get_project_metadata(project_id).get('retention_id', None)
        if retention_id:
            url = "/api/retentions/{retention_id}".format(retention_id=retention_id)
            response = self._send_request(url, headers=self.headers, method="GET")
            return response
        else:
            return None


def setup_module_object():
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
        required_together=[['harbor_username', 'harbor_password']]
    )
    return module


argument_spec = harbor_argument_spec()

argument_spec.update(
    name=dict(type='str', required=True),
    auto_scan=dict(type='bool', defaults=False),
    quota_disk_space=dict(type='int', default=-1),
    quota_artifact_count=dict(type='int', default=-1),
    administrators=dict(type='list', default=None),
)


def main():

    module = setup_module_object()
    state = module.params['state']
    name = module.params['name']
    quota_disk_space = module.params['quota_disk_space']
    quota_artifact_count = module.params['quota_artifact_count']
    administrators = module.params['administrators']
    autoscan = module.params['auto_scan'] is True

    harbor_iface = HarborInterface(module)

    changed = False
    created = False

    if state == 'present':
        project = harbor_iface.get_project_by_name(name)
        if project is None:
            harbor_iface.create_project(name, quota_disk_space, quota_artifact_count)
            project = harbor_iface.get_project_by_name(name)
            created = True
            changed = True

        requested_quota = {"count": quota_artifact_count, "storage": quota_disk_space}
        if requested_quota != project["quota"]["hard"]:
            harbor_iface.update_quota(name, quota_disk_space, quota_artifact_count)
            project = harbor_iface.get_project_by_name(name)
            changed = True

        project_id = project['project_id']
        metadata = harbor_iface.get_project_metadata(project_id)

        if administrators:
            for user_name in administrators:
                members = harbor_iface.get_project_members(project_id)
                if user_name not in [member['entity_name'] for member in members]:
                    harbor_iface.add_admin_member_to_project(user_name, project_id)
                    changed = True
            project = harbor_iface.get_project_by_name(name)

        has_autoscan = metadata.get('auto_scan', "false") == "true"
        if autoscan != has_autoscan:
            harbor_iface.enable_autoscan(project_id, autoscan)
            project = harbor_iface.get_project_by_name(name)
            changed = True

        module.exit_json(failed=False, changed=changed, project=project, created=created)
    elif state == 'absent':
        project = harbor_iface.get_project_by_name(name)
        if project is None:
            module.exit_json(failed=False, changed=False, message="No project found")
        harbor_iface.delete_project(project.get("project_id"))
        module.exit_json(failed=False, changed=True, project=project)


if __name__ == '__main__':
    main()
