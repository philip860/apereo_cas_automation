# CAS SAML Service Ansible Module

## Overview
The `cas_saml_service` Ansible module manages CAS SAML service configurations by creating or removing service registry files.

## Features
- Create or update a CAS SAML service configuration.
- Remove an existing CAS SAML service configuration.
- Validate required parameters before processing.
- Ensure uniqueness of `service_id` within the service registry.

## Requirements
- Ansible 2.9+
- Python 3.x
- The module should be placed in the Ansible `library/` directory or within a custom module path.

## Module Parameters

| Parameter               | Required | Type   | Choices    | Description |
|-------------------------|----------|--------|------------|-------------|
| `state`                 | Yes      | str    | `present`, `absent` | Specifies whether the service should be created (`present`) or removed (`absent`). |
| `entityID`              | No       | str    |            | The unique entity ID for the service. |
| `service_registry_path` | Yes      | str    |            | The path where the service configuration will be stored. |
| `service_id`           | No       | str    |            | A unique identifier for the service (auto-generated if not provided). |
| `service_name`         | No       | str    |            | The name of the service. |
| `service_description`  | No       | str    |            | A brief description of the service. |
| `required_NameId_Format` | No     | str    |            | The required NameID format for SAML authentication. |
| `nameID_Attribute`     | No       | str    |            | The attribute to use as NameID. |
| `attributes`           | No       | dict   |            | A dictionary defining attribute mappings. |

## Usage Examples

### Creating a CAS SAML Service Configuration
```yaml
- name: Create a CAS SAML service configuration
  cas_saml_service:
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
  cas_saml_service:
    state: absent
    service_registry_path: "/etc/cas/saml"
```

## Installation and Execution
1. Copy the `cas_saml_service.py` file into your Ansible `library/` directory.
   ```sh
   mkdir -p ansible/library/
   cp cas_saml_service.py ansible/library/
   ```
2. Ensure the module is executable:
   ```sh
   chmod +x ansible/library/cas_saml_service.py
   ```
3. Run your Ansible playbook:
   ```sh
   ansible-playbook my_playbook.yml
   ```

## Return Values

| Key                | Type   | Description |
|--------------------|--------|-------------|
| `original_message` | dict   | The original parameters provided to the module. |
| `message`          | str    | Status message about the operation performed. |

## License
This module is licensed under the GNU General Public License v3.0+.

## Author
- Your Name (@yourGitHubHandle)

