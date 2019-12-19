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
module: harbor_retention
author:
  - Antoine Gaudelas (!UNKNOWN)
  - Rémi REY (!UNKNOWN)
description:
  - Create/update/delete Harbor projects using Harbor's REST API.
short_description: Create project on Harbor
options:
  project_name:
    description: name of the project
    required: true
    type: str
  rules:
    description: name of the project
    required: false
    type: list
    default: []
  schedule:
    description: name of the project
    required: false
    type: str
    default: ""
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
from ansible.module_utils.common.dict_transformations import recursive_diff
from ansible_collections.sfr.harbor.plugins.module_utils.base import harbor_argument_spec
from ansible_collections.sfr.harbor.plugins.module_utils.harbor import HarborBaseInterface

__metaclass__ = type


class HarborInterface(HarborBaseInterface):

    def get_project_by_name(self, name):
        project = super(HarborInterface, self).get_project_by_name(name)
        if project:
            project_id = project['project_id']
            retention_id = project['metadata'].get("retention_id", None)

            project['retention'] = None
            if retention_id:
                project['retention'] = self.get_retention(retention_id)
        return project

    def get_retention_definition(self, project_id, rules, schedule, trigger_references):
        try:
            rules = [get_rule_definition(project_id, rule) for rule in rules]
        except Exception as e:
            self._module.fail_json(msg=str(e))

        payload = {
            "rules": rules,
            "algorithm": "or",
            "trigger": {
                "kind": "Schedule",
                "settings": {"cron": schedule},
                "references": trigger_references
            },
            "scope": {"level": "project", "ref": project_id}
        }
        return payload

    def create_retention(self, project_id, rules, schedule, trigger_references):
        payload = self.get_retention_definition(project_id, rules, schedule, trigger_references)
        url = "/api/retentions"
        response = self._send_request(url, data=payload, headers=self.headers, method="POST")
        return response

    def update_retention(self, retention_id, project_id, rules, schedule, trigger_references):
        url = "/api/retentions/{id}".format(id=retention_id)
        payload = self.get_retention_definition(project_id, rules, schedule, trigger_references)
        response = self._send_request(url, data=payload, headers=self.headers, method="PUT")
        return response

    def get_retention(self, retention_id):
        url = "/api/retentions/{retention_id}".format(retention_id=retention_id)
        response = self._send_request(url, headers=self.headers, method="GET")
        return response

#    def get_project_retention(self, project_id):
#        retention_id = self.get_project_metadata(project_id).get('retention_id', None)
#        if retention_id:
#            url = "/api/retentions/{retention_id}".format(retention_id=retention_id)
#            response = self._send_request(url, headers=self.headers, method="GET")
#            return response
#        else:
#            return None


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
    rules=dict(type='list', required=False, default=[]),
    schedule=dict(type='str', required=False, default=""),
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


def get_retention_scope_selector(rule):
    if "include_repos" in rule.keys():
        action = "include_repos"
        decoration = "repoMatches"
    elif "exclude_repos" in rule.keys():
        action = "exclude_repos"
        decoration = "repoExcludes"
    else:
        raise Exception("Rule shall contain 'include_repos' or 'exclude_repos' parameter")
    pattern = rule[action]
    return {
        "repository": [
            {
                "kind": "doublestar",
                "decoration": decoration,
                "pattern": pattern
            }
        ]
    }


def get_retention_tag_selector(rule):
    if "include_tags" in rule.keys():
        action = "include_tags"
        decoration = "matches"
    elif "exclude_tags" in rule.keys():
        action = "exclude_tags"
        decoration = "excludes"
    else:
        raise Exception("Rule shall contain 'include_tags' or 'exclude_tags' parameter")
    pattern = rule[action]
    return [{
        "kind": "doublestar",
        "decoration": decoration,
        "pattern": pattern
    }]


def get_rule_definition(project_id, rule):
    if rule["retain"] == -1:
        template = "always"
        params = {}
    else:
        template = "latestPushedK"
        params = {"latestPushedK": rule["retain"]}

    return {
        "disabled": False,
        "action": "retain",
        "params": {"latestPushedK": rule["retain"]},
        "scope_selectors": get_retention_scope_selector(rule),
        "tag_selectors": get_retention_tag_selector(rule),
        "template": template
    }


def main():

    module = setup_module_object()
    project_name = module.params['project_name']
    rules = module.params['rules']
    schedule = module.params['schedule']

    harbor_iface = HarborInterface(module)

    changed = False
    project = harbor_iface.get_project_by_name(project_name)
    if not project:
        module.fail_json(msg="Project '%s' not found" % project_name)

    project_id = project["project_id"]

    if project["retention"] is None:
        trigger_references = {}
        harbor_iface.create_retention(project_id, rules, schedule, trigger_references)
        project = harbor_iface.get_project_by_name(project_name)
        changed = True

    trigger_references = project["retention"]["trigger"]["references"]
    existing_retention = clean_harbor_retention_rules(project["retention"])
    requested_retention = harbor_iface.get_retention_definition(project_id, rules, schedule, trigger_references)

    if existing_retention != requested_retention:
        harbor_iface.update_retention(project["retention"]["id"], project_id, rules, schedule, trigger_references)
        project = harbor_iface.get_project_by_name(project_name)
        changed = True

    diff = recursive_diff(existing_retention, requested_retention)
    module.exit_json(changed=changed, project=project, diff=diff)


if __name__ == '__main__':
    main()
