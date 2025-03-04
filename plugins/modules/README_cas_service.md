# CAS Service Ansible Module

## Overview
The `cas_service` Ansible module manages CAS service configurations by creating or removing service registry files.

## Features
- **Create or Update CAS Service Configurations**: Ensures the configuration file is created or updated based on user inputs.
- **Remove CAS Service Configurations**: Deletes service configuration files when no longer needed.
- **Ensures Unique Service ID**: Prevents duplicate `service_id` entries within the registry.
- **Validates Required Parameters**: Checks for required fields before executing actions.
- **Manages Attribute Release Policies**: Allows attribute mapping for CAS authentication.
- **Handles Non-Existent Directories**: Automatically creates missing service registry directories.
- **Supports Check Mode**: Allows running without making actual changes.

## Module Parameters

| Parameter               | Required | Type   | Choices    | Description |
|-------------------------|----------|--------|------------|-------------|
| `state`                 | Yes      | str    | `present`, `absent` | Specifies whether the service should be created (`present`) or removed (`absent`). |
| `entityID`              | No       | str    |            | The unique entity ID for the service. |
| `service_registry_path` | Yes      | str    |            | The path where the service configuration will be stored. |
| `service_id`           | No       | str    |            | A unique identifier for the service. |
| `service_name`         | No       | str    |            | The name of the service. |
| `service_description`  | No       | str    |            | A brief description of the service. |
| `evaluationOrder`       | No       | int    |            | The evaluation order for the service. Defaults to `1`. |
| `allowed_attributes`   | No       | list   |            | A list of attributes allowed for release in authentication. |

## Usage Examples

### Creating a CAS Service Configuration
```yaml
- name: Create a CAS service configuration
  cas_service:
    state: present
    entityID: "https://stamford.uconn.edu"
    service_id: "10000440"
    service_registry_path: "/etc/cas/services"
    service_name: "stamford.uconn.edu - SSO"
    service_description: "stamford.uconn.edu Prod - Adam Berkowitz"
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
  cas_service:
    state: absent
    service_registry_path: "/etc/cas/services"
    service_id: "10000440"
```
**Note:** When removing a CAS service configuration, make sure to specify the full path to the service file (`service_id`) rather than just the directory.

## Return Values

| Key                | Type   | Description |
|--------------------|--------|-------------|
| `original_message` | dict   | The original parameters provided to the module. |
| `message`          | str    | Status message about the operation performed. |

## License
This module is licensed under the GNU General Public License v3.0+.

## Author
- Your Name (philipduncan860@gmail.com)

