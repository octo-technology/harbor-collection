# -*- coding: utf-8 -*-

# Copyright: (c) 2019, SFR
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    # Standard mysql documentation fragment
    DOCUMENTATION = r'''options:
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
