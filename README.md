# CAS Ansible Collection

## Overview
The `cas_service` and `cas_saml_service` Ansible modules manage CAS service configurations by creating or removing service registry files.

## Features
- **Create or Update CAS Service Configurations**: Ensures the configuration file is created or updated based on user inputs.
- **Remove CAS Service Configurations**: Deletes service configuration files when no longer needed.
- **Ensures Unique Service ID**: Prevents duplicate `service_id` entries within the registry.
- **Validates Required Parameters**: Checks for required fields before executing actions.
- **Manages Attribute Release Policies**: Allows attribute mapping for CAS authentication.
- **Handles Non-Existent Directories**: Automatically creates missing service registry directories.
- **Supports Check Mode**: Allows running without making actual changes.

## Directory Structure
```
ansible_collections/
└── your_namespace/
    └── your_collection/
        ├── README.md
        ├── plugins/
        │   ├── modules/
        │   │   ├── cas_service.py
        │   │   ├── cas_saml_service.py
        │   │   ├── README_cas_service.md
        │   │   ├── README_cas_saml_service.md
        ├── docs/
        │   ├── README_cas_service.md
        │   ├── README_cas_saml_service.md
        ├── galaxy.yml
        ├── meta/
        ├── tests/
        ├── roles/
```

## Included Modules
- [`cas_service`](docs/README_cas_service.md) - Manages CAS service configurations.
- [`cas_saml_service`](docs/README_cas_saml_service.md) - Manages CAS SAML authentication configurations.

## Module Parameters
Refer to the individual module documentation:
- [`cas_service`](docs/README_cas_service.md)
- [`cas_saml_service`](docs/README_cas_saml_service.md)

## Usage Examples

### Creating a CAS Service Configuration
```yaml
- name: Create a CAS service configuration
  philip860.apereo_cas.cas_service:
    state: present
    entityID: "https://stamford.uconn.edu"
    service_id: "10000440"
    service_registry_path: "/etc/cas/services"
    service_name: "stamford.uconn.edu - SSO"
    service_description: "stamford.uconn.edu Prod - Phil Duncan"
    evaluationOrder: 1
    allowed_attributes:
      - netid
      - givenName
      - sn
      - uconnPersonAffiliation
      - email
```

### Removing a CAS Service Configuration
```yaml
- name: Remove a CAS service configuration
  philip860.apereo_cas.cas_service:
    state: absent
    service_registry_path: "/etc/cas/services/service_10000440.json"
```

### Creating a CAS SAML Service Configuration
```yaml
- name: Create a CAS SAML service configuration
  philip860.apereo_cas.cas_saml_service:
    state: present
    entityID: "http://sso.example.com/shibboleth"
    service_registry_path: "/etc/cas/saml"
    service_id: "100001"
    service_name: "Example SSO"
    service_description: "Example SSO Service"
    required_NameId_Format: "urn:oasis:names:tc:SAML:2.0:nameid-format:unspecified"
    nameID_Attribute: "uid"
    attributes:
      uid: "netid"
      email: "EmailAddress"
      displaySn: "LastName"
      givenName: "FirstName"
```

### Removing a CAS SAML Service Configuration
```yaml
- name: Remove a CAS SAML service configuration
  philip860.apereo_cas.cas_saml_service:
    state: absent
    service_registry_path: "/etc/cas/saml/service_10000538.json"
```
**Note:** When removing a CAS service configuration, ensure that the full path to the service file is specified to avoid unintended deletions.

## Return Values
| Key                | Type   | Description |
|--------------------|--------|-------------|
| `original_message` | dict   | The original parameters provided to the module. |
| `message`          | str    | Status message about the operation performed. |

## License
This module is licensed under the GNU General Public License v3.0+.

## Author
- Your Name (philipduncan860@gmail.com)

