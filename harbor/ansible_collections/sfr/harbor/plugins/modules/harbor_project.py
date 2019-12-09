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
module: harbor.projects

description:
  - Create/update/delete Harbor projects using Harbor's REST API.
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
'''

RETURN = '''
---
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
        if status_code == 404 or status_code == 201:
            return None
        elif status_code == 200:
            content = resp.read()
            if content:
                return self._module.from_json(content)
            else:
                return None
        elif status_code == 401:
            self._module.fail_json(msg="Unauthorized to perform action '%s' on '%s' header: %s" % (method, full_url, self.headers))
        elif status_code == 403:
            self._module.fail_json(msg="Permission Denied")
        self._module.fail_json(
            failed=True,
            msg="Harbor API answered with HTTP %d, url %s, response %s, payload %s" % (status_code, full_url, resp, data))

    def create_project(self, name):
        url = "/api/projects"
        project = dict(project_name=name, metadata=dict(public="false"), count_limit=-1, storage_limit=10737418240)
        response = self._send_request(url, data=project, headers=self.headers, method="POST")
        return response

    def get_project_by_name(self, name):
        url = "/api/projects?name={name}".format(name=name)
        response = self._send_request(url, headers=self.headers, method="GET")

        if not response:
            return None

        if not len(response) == 1:
            raise AssertionError("Expected 1 project, got %d" % len(response))

        return response[0]

    def delete_project(self, project_id):
        url = "/api/projects/{project_id}".format(project_id=project_id)
        response = self._send_request(url, headers=self.headers, method="DELETE")
        return response

    def get_project_members(self):
        pass

    def add_admin_member_to_project(self):
        pass

    def enable_autoscan(self):
        pass

    def retain_versioned_images_in_project(self):
        pass


def setup_module_object():
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
        required_together=[['harbor_username', 'harbor_password']]
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
    harbor_url=dict(type='str', required=True),
    harbor_username=dict(aliases=['harbor_user'], type='str'),
    harbor_password=dict(type='str'),
)


def main():

    module = setup_module_object()
    state = module.params['state']
    name = module.params['name']

    harbor_iface = HarborInterface(module)

    changed = False
    if state == 'present':
        project = harbor_iface.get_project_by_name(name)
        if project is None:
            harbor_iface.create_project(name)
            project = harbor_iface.get_project_by_name(name)
            changed = True
        module.exit_json(failed=False, changed=changed, project=project)
    elif state == 'absent':
        project = harbor_iface.get_project_by_name(name)
        if project is None:
            module.exit_json(failed=False, changed=False, message="No project found")
        harbor_iface.delete_project(project.get("project_id"))
        module.exit_json(failed=False, changed=True, project=project)


if __name__ == '__main__':
    main()