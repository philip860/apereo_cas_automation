# CAS SAML Service Ansible Module

## Overview
The `cas_saml_service` Ansible module manages CAS SAML service configurations by creating or removing service registry files.

## Features
- **Create or Update CAS SAML Service Configurations**: Ensures the configuration file is created or updated based on user inputs.
- **Remove CAS SAML Service Configurations**: Deletes service configuration files when no longer needed.
- **Ensures Unique Service ID**: Prevents duplicate `service_id` entries within the registry.
- **Validates Required Parameters**: Checks for required fields before executing actions.
- **Manages SAML Attributes**: Allows attribute mapping for SAML authentication.
- **Supports Custom Metadata Location**: Enables specifying external metadata files.
- **Handles Non-Existent Directories**: Automatically creates missing service registry directories.
- **Supports Check Mode**: Allows running without making actual changes.

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

## Return Values

| Key                | Type   | Description |
|--------------------|--------|-------------|
| `original_message` | dict   | The original parameters provided to the module. |
| `message`          | str    | Status message about the operation performed. |

## License
This module is licensed under the GNU General Public License v3.0+.

## Author
- Your Name (@philipduncan860@gmail.com)

