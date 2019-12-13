# -*- coding: utf-8 -*-
#
# Copyright: (c) 2019, SFR
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.urls import url_argument_spec

__metaclass__ = type


def harbor_argument_spec():
    argument_spec = url_argument_spec()

    del argument_spec['force']
    del argument_spec['force_basic_auth']
    del argument_spec['http_agent']

    argument_spec.update(
        state=dict(choices=['present', 'absent'], default='present'),
        url=dict(aliases=['harbor_url'], type='str', required=True),
        url_username=dict(aliases=['harbor_user'], type='str', default="admin"),
        url_password=dict(aliases=['harbor_password'], type='str', default="Harbor12345")
    )
    return argument_spec
