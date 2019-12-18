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
  versions_retained:
    description: number of semantically tagged versions of images to retain (last pushed)
    required: false
    type: int
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
  - sfr.harbor.harbor
'''

EXAMPLES = '''
- name: set retention to 10 semantically versioned image versions
  harbor_retention:
    harbor_url: "http://{{ local_harbor }}"
    harbor_username: "{{ harbor_admin_user }}"
    harbor_password: "{{ harbor_admin_password }}"
    project_name: test_project
    rules:
      - include_repos: "**"
        include_tags:  "*.*.*"
        retain: 10

- name: set retention to always retain semantically versioned image versions
  harbor_retention:
    harbor_url: "http://{{ local_harbor }}"
    harbor_username: "{{ harbor_admin_user }}"
    harbor_password: "{{ harbor_admin_password }}"
    project_name: test_project
    rules:
      - include_repos: "**"
        include_tags:  "*.*.*"
        retain: always

- name: set retention to retain 5 last versioned images and 3 non versioned
  harbor_retention:
    harbor_url: "http://{{ local_harbor }}"
    harbor_username: "{{ harbor_admin_user }}"
    harbor_password: "{{ harbor_admin_password }}"
    project_name: test_project
    rules:
      - include_repos: "**"
        include_tags:  "*.*.*"
        retain: 5
      - include_repos: "**"
        exclude_tags:  "*.*.*"
        retain: 3
'''

RETURN = '''
---
'''

import itertools
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.sfr.harbor.plugins.module_utils.base import harbor_argument_spec
from ansible_collections.sfr.harbor.plugins.module_utils.harbor import HarborBaseInterface

__metaclass__ = type


class HarborInterface(HarborBaseInterface):


    def get_project_by_name(self, name):
        project = super(HarborInterface, self).get_project_by_name(name)
        if project:
            project_id = project['project_id']
            project['retention'] = self.get_project_retention(project_id)
        return project


    def get_rule_definition(self, project_id, rule):
        return {
                "disabled": False,
                "action": "retain",
                "params": {"latestPushedK": 1},
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

    def get_retention_definition(self, project_id, rules):
        payload = {
            "rules": [self.get_rule_definition(project_id, rule) for rule in rules],
            "algorithm": "or",
            "trigger": {
                "kind": "Schedule",
                "references": {},
                "settings": {"cron": ""}
            },
            "scope": {"level": "project", "ref": project_id}
        }
        return payload

    def create_retention(self, project_id, rules):
        payload = self.get_retention_definition(project_id, rules)
        url = "/api/retentions"
        response = self._send_request(url, data=payload, headers=self.headers, method="POST")
        return response

    def update_retention(self, retention_id, project_id, rules):
        payload = self.get_retention_definition(project_id, rules)
        url = "/api/retentions/{id}".format(id=retention_id)
        response = self._send_request(url, data=payload, headers=self.headers, method="PUT")
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
    project_name=dict(type='str', required=True),
    rules=dict(type=list, required=False, default=[]),
)


def clean_harbor_retention_rules(project_retention):
    # remove server-generated keys to allow for memberwise comparison
    clean_retention = {}
    for k, v in project_retention.items():
        if k != "id":
            clean_retention[k] = v
    for rule in clean_retention['rules']:
        del rule["id"]
        del rule["priority"]
    return clean_retention


def main():

    module = setup_module_object()
    project_name = module.params['project_name']
    rules = module.params['rules']

    harbor_iface = HarborInterface(module)

    changed = False
    project = harbor_iface.get_project_by_name(project_name)
    if not project:
        module.fail_json(msg="Project '%s' not found" % project_name)

    project_id = project["project_id"]
    existing_retention = clean_harbor_retention_rules(project["retention"])
    requested_retention = harbor_iface.get_retention_definition(project_id, rules)

    if existing_retention == requested_retention:
        module.exit_json(changed=False, project=project, msg="no changes")
    else:
        if existing_retention:
            harbor_iface.update_retention(project["retention"]["id"], project_id, rules)
        else:
            harbor_iface.create_retention(project_id, rules)
        project = harbor_iface.get_project_by_name(project_name)
        changed = True

    module.exit_json(failed=False, changed=changed, project=project)


if __name__ == '__main__':
    main()
