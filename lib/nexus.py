import requests
import string
import logging
import random
import time

# Debug
debug = False


def post_json(url, user, password, data):
    """
    HTTP Post Request

    Args:
        name = Context Name (string)
        docker_port = Portnummer fuer das Nexus Docker Repo (int)
        data = Native API Call (dict)

    Returns:
        API Schema (dict)
    """
    api_url = url + "/service/extdirect"
    auth_values = (user, password)
    response = requests.post(api_url, json=data, auth=auth_values)
    response_output = response.json()
    response_success = response_output["result"]["success"]

    time.sleep(1)
    if response_success:
        return "ok"
    else:
        return "failed"


def create_repo(param, user, password, url):
    """
    Nexus Repository anlegen

    Args:
        param = Schema siehe schema.nexus (dict)
        user = API Username (string)
        password = API Password (string)
        url = API URL (string)

    Returns:
        True/False
    """
    success = True
    for repo_name in param:
        repo_type = param[repo_name]["type"]
        if repo_type == "docker":
            # Docker repository
            repo_port = param[repo_name]["port"]

            api_call = {
                "action": "coreui_Repository",
                "method": "create",
                "data": [
                    {
                        "attributes": {
                            "docker": {
                                "httpsPort": repo_port,
                                "forceBasicAuth": "true",
                                "v1Enabled": "true"
                            },
                            "storage": {
                                "blobStoreName": "default",
                                "strictContentTypeValidation": "true",
                                "writePolicy": "ALLOW"
                            },
                            "cleanup": {
                                "policyName": "None"
                            }
                        },
                        "name": repo_name,
                        "format": "",
                        "type": "",
                        "url": "",
                        "online": "true",
                        "undefined": [
                            "false",
                            "true"
                        ],
                        "recipe": "docker-hosted"
                    }
                ],
                "type": "rpc",
                "tid": random.randint(1, 101)
            }
        elif repo_type == "raw":
            # Raw Repository
            api_call = {
                "action": "coreui_Repository",
                "method": "create",
                "data": [
                    {
                        "attributes": {
                            "storage": {
                                "blobStoreName": "default",
                                "strictContentTypeValidation": "false",
                                "writePolicy": "ALLOW"
                            },
                            "cleanup": {
                                "policyName": "None"
                            }
                        },
                        "name": repo_name,
                        "format": "",
                        "type": "",
                        "url": "",
                        "online": "true",
                        "recipe": "raw-hosted"
                    }
                ],
                "type": "rpc",
                "tid": random.randint(1,101)
            }

        else:
            raise Exception('Nexus Repository type unkown')

        msg = "NEXUS Anlegen " + repo_type + " Repository " + repo_name
        result = post_json(url=url, user=user, password=password, data=api_call)
        logging.info(msg)
        if result != "ok":
            logging.error(msg)
            success = False

    return success


def delete_repo(param, user, password, url):
    """
    Nexus Repository loeschen

    Args:
        param = Schema siehe schema.nexus (dict)
        user = API Username (string)
        password = API Password (string)
        url = API URL (string)

    Returns:
        True/False
    """
    success = True
    for repo_name in param:
        repo_type = param[repo_name]["type"]

        api_call = {
            "action": "coreui_Repository",
            "method": "remove",
            "data": [repo_name],
            "type": "rpc",
            "tid": random.randint(1,101)
        }
        msg = "NEXUS Loesche " + repo_type + " Repository " + repo_name
        result = post_json(url=url, user=user, password=password, data=api_call)
        logging.info(msg)
        if result != "ok":
            logging.error(msg)
            success = False

    return success


def create_role(param, user, password, url):
    """
    Nexus Rolle anlegen

    Args:
        param = Schema siehe schema.nexus (dict)
        user = API Username (string)
        password = API Password (string)
        url = API URL (string)

    Returns:
        True/False
    """
    success = True
    for role_name in sorted(param):
        role_privileges = param[role_name]["privileges"]
        role_contained = param[role_name]["contained_roles"]

        api_call = {
            "action": "coreui_Role",
            "method": "create",
            "data": [
                {
                    "version": "",
                    "source": "default",
                    "id": role_name,
                    "name": role_name,
                    "description": role_name,
                    "privileges": role_privileges,
                    "roles": role_contained
                }
            ],
            "type": "rpc",
            "tid": random.randint(1,101)
        }
        msg = "NEXUS Anlegen Role " + role_name
        logging.info(msg)
        result = post_json(url=url, user=user, password=password, data=api_call)
        if result != "ok":
            logging.error(msg)
            success = False

    return success


def delete_role(param, user, password, url):
    """
    Nexus Repository loeschen

    Args:
        param = Schema siehe schema.nexus (dict)
        user = API Username (string)
        password = API Password (string)
        url = API URL (string)

    Returns:
        True/False
    """
    success = True
    for role_name in sorted(param):
        api_call = {
            "action": "coreui_Role",
            "method": "remove",
            "data": [role_name],
            "type": "rpc",
            "tid": random.randint(1, 101)
        }

        msg = "NEXUS Loesche Role " + role_name
        logging.info(msg)
        result = post_json(url=url, user=user, password=password, data=api_call)
        if result != "ok":
            logging.error(msg)
            success = False

    return success


def create_user(users, user, password, url):
    """
    Nexus User anlegen

    Args:
        param = Schema siehe schema.nexus (dict)
        user = API Username (string)
        password = API Password (string)
        url = API URL (string)

    Returns:
        True/False
    """
    success = True
    for user_name in users:
        allchar = string.ascii_letters + string.digits
        user_pass = "".join(random.choice(allchar) for x in range(random.randint(12, 16)))
        user_role = users[user_name]["role"]

        api_call = {
            "action": "coreui_User",
            "method": "create",
            "data": [
                {
                    "userId": user_name,
                    "version": "",
                    "firstName": user_name,
                    "lastName": user_name,
                    "email": user_name + "@no.email",
                    "status": "active",
                    "roles": user_role,
                    "password": user_pass
                }
            ],
            "type": "rpc",
            "tid": random.randint(1,101)
        }

        msg = "NEXUS Anlegen User " + user_name
        logging.info(msg)
        result = post_json(url=url, user=user, password=password, data=api_call)
        if result != "ok":
            logging.error(msg)
            success = False

    return success


def delete_user(users, user, password, url):
    """
    Nexus User loeschen

    Args:
        users = Nexus User (array)
        user = API Username (string)
        password = API Password (string)
        url = API URL (string)

    Returns:
        True/False
    """
    success = True
    for user_name in users:
        api_call = {
            "action": "coreui_User",
            "method": "remove",
            "data": [user_name, "default"],
            "type": "rpc",
            "tid": random.randint(1, 101)
        }

        msg = "NEXUS Loesche User " + user_name
        logging.info(msg)
        result = post_json(url=url, user=user, password=password, data=api_call)
        if result != "ok":
            logging.error(msg)
            success = False

    return success
