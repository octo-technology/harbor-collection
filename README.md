# Ansible Collection - sfr.harbor

Harbor collection by SFR

## Release Process

The Gitlab pipeline will automatically test and build the collection for every Merge Request.
The collection is published on Nexus only when a Tag is created on the repository.

**CAUTION:** The `galaxy.yml` MUST be updated to have its `version` parameter updated with the futire tag value.
The `ansible-galaxy` build command is building the collection archive based on the `galaxy.yml`
content (and no argument is available to dynamically provide the version).

## Modules

### harbor_user

The module allows to manage Users in Harbor. It shall not be used if ldap is plugged in.

### harbor_project

The module allows to manage Projects in Harbor.

### harbor_retention

The module allows to manage Projects Tag retention rules in Harbor.

## Modules documentation

All the modules are documented through the standard Ansible method: Through the `DOCUMENTATION` variable inside the module.
This method allows to used the `ansible-doc` command.:


Example ; With the collection installed :
```
$ ansible-doc sfr.harbor.harbor_project
```

## Development

### Tests

Official documentation on Collections development can be found [here](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html)

Tests can be executed against the collection with `ansible-test`, which was released with `ansible` in version `2.9.0`. 
The following commands will require version `2.9.0` as a minimal Ansible version.

#### Sanity tests

Sanity tests allows to run several tools like pylint and pep8 conformity tests.
The tests also check that the modules documentation reflects the reality of the module implementation (checks defaults, aliases, etc ...)

You can run the sanity tests by executing the following command:

```
$ ansible-test sanity
```

or using docker (prefered):

```
$ ansible-test sanity --docker
```

#### Unit tests

Unit tests allows to tests the plugins code through `pytest`.
**The harbor collection does not contain any unit tests yet**

```
$ ansible-test units
``` 

or using docker (prefered):

```
$ ansible-test units --docker
``` 

#### Integration tests

Integration tests allows to execute tests against a running instance of Harbor.
The Harbor instance creation is not handled by the `ansible-test` command, and shall be handled before running the command.

Once the instance ready, you can run the integration tests by executing the following command:

```
$ ansible-test integration
```

or using docker (prefered):

```
$ ansible-test integration --docker
```

##### Integration test targets

The integration tests have notions of targets. 
A target is a set of tests which are represented as ansible roles in the `tests/integration/targets/` directory.

When running the `ansible-test integration` command, the command will run all targets. One can execute a specific target
by specifying the target name in the command :

Example: Running the `harbor_project` target.
```
$ ansible-test integration harbor_project
```

## Requirements

The `requirements.txt` at the base of the git repository is only for the development environment.
**The collection usage does not require any dependency**
