#!/usr/bin/python

# Copyright: (c) 2025, Your Name <your.email@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import os
import random
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r'''
---
module: cas_service

short_description: Manages CAS service configurations

version_added: "1.0.0"

description:
    - Creates or removes a CAS service configuration file.

options:
    state:
        description:
            - Specifies the action to perform.
            - "present" to create/update a service file.
            - "absent" to remove a service file.
        required: true
        choices: ["present", "absent"]
        type: str

    entityID:
        description: The unique entity ID for the CAS service.
        required: false
        type: str

    service_id:
        description: The unique ID for the CAS service.
        required: false
        type: str

    service_registry_path:
        description: Path to the CAS service registry directory.
        required: true
        type: str

    service_name:
        description: The name of the service.
        required: false
        type: str

    service_description:
        description: A brief description of the service.
        required: false
        type: str

    evaluationOrder:
        description: Evaluation order of the service.
        required: false
        type: int
        default: 1

    allowed_attributes:
        description: List of allowed attributes for the service.
        required: false
        type: list
        elements: str
        default: []

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
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

- name: Remove a CAS service configuration
  cas_service:
    state: absent
    service_registry_path: "/etc/cas/services"
    service_id: "10000440"
'''

RETURN = r'''
original_message:
    description: The original parameters provided.
    type: dict
    returned: always

message:
    description: Status message about the operation.
    type: str
    returned: always
'''

def run_module():
    module_args = dict(
        state=dict(type='str', required=True, choices=['present', 'absent']),
        entityID=dict(type='str', required=False),
        service_id=dict(type='str', required=False),
        service_registry_path=dict(type='str', required=True),
        service_name=dict(type='str', required=False),
        service_description=dict(type='str', required=False),
        evaluationOrder=dict(type='int', required=False, default=1),
        allowed_attributes=dict(type='list', elements='str', required=False, default=[]),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    state = module.params['state']
    service_registry_path = module.params['service_registry_path']
    service_id = module.params['service_id'] if module.params['service_id'] else str(random.randint(1000, 9999))

    if state == 'present':
        required_params = ['entityID', 'service_id', 'service_description', 'allowed_attributes']
        missing_params = [param for param in required_params if not module.params.get(param)]
        if missing_params:
            module.fail_json(msg=f"Missing required parameters for state=present: {', '.join(missing_params)}")

        if not os.path.exists(service_registry_path):
            os.makedirs(service_registry_path)
        
        if not os.path.isdir(service_registry_path):
            module.fail_json(msg=f"{service_registry_path} exists but is not a directory.")

        for filename in os.listdir(service_registry_path):
            file_path = os.path.join(service_registry_path, filename)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if str(data.get("id")) == service_id:
                            module.fail_json(msg=f"Service ID {service_id} is already in use in {file_path}.")
                except json.JSONDecodeError:
                    continue
        
        
        service_data = {
            "@class": "org.apereo.cas.services.CasRegisteredService",
            "serviceId": module.params['entityID'],
            "name": module.params['service_name'],
            "id": service_id,
            "evaluationOrder": int(service_id),
            "description": module.params['service_description'],
            "attributeReleasePolicy": {
                "@class": "org.apereo.cas.services.ReturnAllowedAttributeReleasePolicy",
                "allowedAttributes": [
                    "java.util.ArrayList", module.params['allowed_attributes']
                ]
            }
        }

        new_service_file = os.path.join(service_registry_path, f"service_{service_id}.json")
        with open(new_service_file, 'w') as f:
            json.dump(service_data, f, indent=2)

        #Setting EntityID Variable
        entity_id = module.params['entityID']

        module.exit_json(changed=True, message=f"Service configuration for {entity_id} created at {new_service_file}.")

    elif state == 'absent':
        if not os.path.exists(service_registry_path):
            module.exit_json(changed=False, message=f"Path does not exist: {service_registry_path}")

        try:
            if os.path.isfile(service_registry_path) or os.path.islink(service_registry_path):
                os.remove(service_registry_path)
                module.exit_json(changed=True, message=f"Deleted Service Registry File: {service_registry_path}")
            elif os.path.isdir(service_registry_path):
                try:
                    os.rmdir(service_registry_path)
                    module.exit_json(changed=True, message=f"Deleted empty directory: {service_registry_path}")
                except OSError:
                    shutil.rmtree(service_registry_path)
                    module.exit_json(changed=True, message=f"Deleted non-empty directory and its contents: {service_registry_path}")
        except PermissionError:
            module.fail_json(msg=f"Permission denied: Unable to delete {service_registry_path}")
        except Exception as e:
            module.fail_json(msg=f"Failed to delete {service_registry_path}: {str(e)}")

def main():
    run_module()

if __name__ == '__main__':
    main()
