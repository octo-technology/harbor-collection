# Harbor Collection for Ansible

This repo hosts the `octo.harbor` Ansible Collection.

The collection includes a variety of Ansible content to help automate the management of Harbor resources.

## Included content

Click on the name of a plugin or module to view that content's documentation:

  - **Connection Plugins**:
  - **Filter Plugins**:
  - **Inventory Source**:
  - **Lookup Plugins**:
  - **Modules**:
    - [harbor_project](#)
    - [harbor_retention](#)
    - [harbor_user](#)

## Installation and Usage

### Installing the Collection from Ansible Galaxy

Before using the Kuberentes collection, you need to install it with the Ansible Galaxy CLI:

    ansible-galaxy collection install octo.harbor

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: octo.harbor
    version: 0.1.0
```

### Using modules from the Harbor Collection in your playbooks

You can either call modules by their Fully Qualified Collection Namespace (FQCN), like `octo.harbor.harbor_project`, or you can call modules by their short name if you list the `octo.harbor` collection in the playbook's `collections`, like so:

```yaml
---
- hosts: localhost
  gather_facts: false
  connection: local

  collections:
    - octo.harbor

  tasks:
      harbor_project:
        harbor_url: "https://{{ harbor_url }}"
        harbor_username: "{{ harbor_admin_user }}"
        harbor_password: "{{ harbor_admin_password }}"
        name: test_project
        state: present
```

For documentation on how to use individual modules and other content included in this collection, please see the links in the 'Included content' section earlier in this README.

## Testing and Development

If you want to develop new content for this collection or improve what's already here, the easiest way to work on the collection is to clone it into one of the configured [`COLLECTIONS_PATHS`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths), and work on it there.

### Testing with `ansible-test`

The `tests` directory contains configuration for running sanity and integration tests using [`ansible-test`](https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html).

You can run the collection's test suites with the commands:

    ansible-test sanity --docker -v --color
    ansible-test integration --docker -v --color

## Publishing New Versions

The current process for publishing new versions of the Harbor Collection is manual, and requires a user who has access to the `octo.harbor` namespace on Ansible Galaxy to publish the build artifact.
  1. Ensure `CHANGELOG.md` contains all the latest changes.
  2. Update `galaxy.yml` and this README's `requirements.yml` example with the new `version` for the collection.
  3. Tag the version in Git and push to GitHub.
  4. Run the following commands to build and release the new version on Galaxy:

     ```
     ansible-galaxy collection build
     ansible-galaxy collection publish ./octo-harbor-$VERSION_HERE.tar.gz
     ```

After the version is published, verify it exists on the [Harbor Collection Galaxy page](https://galaxy.ansible.com/octo/harbor).

## License

GNU General Public License v3.0 or later

See LICENCE to see the full text.
