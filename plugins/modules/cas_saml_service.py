#!/usr/bin/python

# Copyright: (c) 2025, Your Name <your.email@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import os
import shutil
import random
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r'''
---
module: cas_saml_service

short_description: Manages CAS SAML service configurations

version_added: "1.0.0"

description:
    - Creates or removes a CAS SAML service configuration file.

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
        description: The unique entity ID for the service.
        required: false
        type: str

    service_registry_path:
        description: Path to the CAS service registry directory.
        required: true
        type: str

    service_id:
        description: The unique ID for the service.
        required: false
        type: str

    service_name:
        description: The name of the service.
        required: false
        type: str

    service_description:
        description: A brief description of the service.
        required: false
        type: str

    required_NameId_Format:
        description: Required NameID format.
        required: false
        type: str

    nameID_Attribute:
        description: Attribute to use as NameID.
        required: false
        type: str

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
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
      "uid": "netid"
      "email": "EmailAddress"
      "displaySn": "LastName"
      "giveName": "FirstName"
  

- name: Remove a CAS SAML service configuration
  cas_saml_service:
    state: absent
    service_registry_path: "/etc/cas/saml"
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
        service_registry_path=dict(type='str', required=True),
        service_id=dict(type='str', required=False),
        metadata_location=dict(type='str', required=False),
        service_name=dict(type='str', required=False),
        service_description=dict(type='str', required=False),
        required_NameId_Format=dict(type='str', required=False),
        nameID_Attribute=dict(type='str', required=False),
        attributes=dict(type='dict', required=False, default={})
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    state = module.params['state']
    service_registry_path = module.params['service_registry_path']
    service_id = module.params['service_id'] if module.params['service_id'] else str(random.randint(1000, 9999))

    # Ensure required parameters are correctly validated
    if state == 'present':
        required_params = ['entityID', 'service_description', 'required_NameId_Format', 'nameID_Attribute', 'metadata_location']
        missing_params = [param for param in required_params if not isinstance(module.params.get(param), str)]
        if missing_params:
            module.fail_json(msg=f"Missing or invalid parameters for state=present: {', '.join(missing_params)}")

        # Ensure attributes is a dictionary
        attributes = module.params.get('attributes', {})
        if not isinstance(attributes, dict):
            module.fail_json(msg="Invalid type for 'attributes': Expected dict, got {}".format(type(attributes).__name__))

        # Ensure service registry path exists
        if not os.path.exists(service_registry_path):
            os.makedirs(service_registry_path, exist_ok=True)

        if not os.path.isdir(service_registry_path):
            module.fail_json(msg=f"{service_registry_path} exists but is not a directory.")

        # Check for duplicate service_id
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
        
        structured_attributes = [
            {"attribute_name": key, "attribute_urn": value} for key, value in attributes.items()
        ]
        
        service_data = {
            "@class": "org.apereo.cas.support.saml.services.SamlRegisteredService",
            "serviceId": module.params['entityID'],
            "name": module.params['service_name'],
            "id": service_id,
            "evaluationOrder": int(service_id),
            "metadataLocation": module.params['metadata_location'],
            "description": module.params['service_description'],
            "requiredNameIdFormat": module.params['required_NameId_Format'],
            "attributeNameFormats": {
                "@class": "java.util.HashMap",
                **{attr["attribute_urn"]: "uri" for attr in structured_attributes}
            },
            "usernameAttributeProvider": {
                "@class": "org.apereo.cas.services.PrincipalAttributeRegisteredServiceUsernameProvider",
                "usernameAttribute": module.params['nameID_Attribute']
            },
            "attributeValueTypes": {
                "@class": "java.util.HashMap",
                **{attr["attribute_urn"]: "XSString" for attr in structured_attributes}
            },
            "attributeReleasePolicy": {
                "@class": "org.apereo.cas.services.ReturnAllowedAttributeReleasePolicy",
                "allowedAttributes": [
                    "java.util.ArrayList",
                    [attr["attribute_name"] for attr in structured_attributes]
                ]
            }
        }
        
        new_service_file = os.path.join(service_registry_path, f"service_{service_id}.json")
        with open(new_service_file, 'w') as f:
            json.dump(service_data, f, indent=2)
        
        module.exit_json(changed=True, message=f"Service configuration {service_id} created at {new_service_file}.")

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
