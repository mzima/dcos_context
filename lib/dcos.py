#!/usr/bin/python

import re
import requests
import logging

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

ssl_verify = False


def post(param, url, token):
    """
    HTTP-Post Request

    Args:
        param = DCOS Native API Request (dict)
        url = DCOS URL (string)
        token = DCOS Token (string)

    Returns:
        HTTP-Statuscode des Request
    """
    auth_header = {"Authorization": "token=" + token}
    response = requests.post(url, json=param, headers=auth_header, verify=ssl_verify, proxies="")
    response_status = str(response.status_code)
    return response_status


def put(param, url, token):
    """
    HTTP-Put Request

    Args:
        param = DCOS Native API Request (dict)
        url = DCOS URL (string)
        token = DCOS Token (string)

    Returns:
        HTTP-Statuscode des Request
    """
    auth_header = {"Authorization": "token=" + token}
    response = requests.put(url, json=param, headers=auth_header, verify=ssl_verify, proxies="")
    response_status = str(response.status_code)
    return response_status


def delete(param, url, token):
    """
    HTTP-Delete Request

    Args:
        param = DCOS Native API Request (dict)
        url = DCOS URL (string)
        token = DCOS Token (string)

    Returns:
        HTTP-Statuscode des Request
    """
    auth_header = {"Authorization": "token=" + token}
    response = requests.delete(url, json=param, headers=auth_header, verify=ssl_verify, proxies="")
    response_status = str(response.status_code)
    return response_status


def get_token(url, user, password):
    """
    DCOS Access Token Anfordern

    Args:
        url = DCOS URL (string)
        user = DCOS User (string)
        password = DCOS Password (string)

    Returns:
        Access Token
    """
    api_call = {
        "uid": user,
        "password": password
    }
    msg = "DC/OS Generiere API Token"
    logging.info(msg)
    api_auth = (user, password)
    api_url = url + "/acs/api/v1/auth/login"

    try:
        response = requests.post(url=api_url, json=api_call, auth=api_auth, verify=ssl_verify)
        response_output = response.json()
        token = str(response_output["token"])
        return token
    except:
        logging.error("DC/OS Unable to obtain API token from " + api_url)


def create_service_group(param, url, token):
    """
    DCOS Service Gruppe anlegen

    Args:
        param = DCOS Native API Request (dict: siehe lib/schema.py)
        url = DCOS URL (string)
        token = DCOS Token (string)

    Returns:
        HTTP-Statuscode des Request
    """
    success = True
    api_url = url + "/service/marathon/v2/groups"
    msg = "DC/OS Anlegen Service Group " + param['id']
    logging.info(msg)
    status = post(param=param, url=api_url, token=token)
    if status not in ["201", "409"]:
        logging.error(msg)
        success = False

    return success


def delete_service_group(param, url, token):
    """
    DCOS Service Gruppe loeschen

    Args:
        param = DCOS Native API Request (dict: siehe lib/schema.py)
        url = DCOS URL (string)
        token = DCOS Token (string)

    Returns:
        HTTP-Statuscode des Request
    """
    success = True
    api_url = url + "/service/marathon/v2/groups/" + param
    msg = "DC/OS Loesche Service Group " + param
    logging.info(msg)
    status = delete(param=param, url=api_url, token=token)

    if status not in ["200"]:
        logging.error(msg)
        success = False

    return success


def create_user_group(param, url, token):
    """
    DCOS User Gruppe anlegen

    Args:
        param = DCOS Native API Request (dict: siehe lib/schema.py)
        url = DCOS URL (string)
        token = DCOS Token (string)

    Returns:
        HTTP-Statuscode des Request
    """
    success = True
    api_url = url + "/acs/api/v1/groups"
    for gid in param:
        msg = "DC/OS Anlegen User Group " + gid
        logging.info(msg)
        status = put(param={"description": gid}, url=api_url + "/" + gid, token=token)

        if status not in ["201", "409"]:
            logging.error(msg)
            success = False

    return success


def delete_user_group(param, url, token):
    """
    DCOS Service Gruppe loeschen

    Args:
        param = DCOS Native API Request (dict: siehe lib/schema.py)
        url = DCOS URL (string)
        token = DCOS Token (string)

    Returns:
        HTTP-Statuscode des Request
    """
    success = True
    api_url = url + "/acs/api/v1/groups"
    for gid in param:
        msg = "DC/OS Loesche User Group " + gid
        logging.info(msg)
        status = delete(param={"description": gid}, url=api_url + "/" + gid, token=token)

        if status not in ["204"]:
            logging.error(msg)
            success = False

    return success


def create_user_group_acl(param, gid, url, token):
    """
    DCOS User Gruppen ACL anlegen

    Args:
        param = DCOS Native API Request (siehe lib/schema.py)
        gid = User Gruppen Name (string)
        url = DCOS URL (string)
        token = DCOS Token (string)

    Returns:
        HTTP-Statuscode des Request
    """
    success = True
    api_url = url + "/acs/api/v1/acls"
    msg = "DC/OS Anlegen Permissions fuer Group " + gid
    logging.info(msg)
    for rid, actions in param.items():
        rid = re.sub('/', '%252F', rid)
        status = put(param={"description": "string"}, url=api_url + "/" + rid, token=token)

        if status not in ["201", "409"]:
            logging.error(msg)

    for rid, actions in param.items():
        rid_masked = re.sub('/', '%252F', rid)
        for action in actions:
            api_call = "/" + rid_masked + "/groups/" + gid + "/" + action
            status = put(param={}, url=api_url + api_call, token=token)

            if status not in ["204", "409"]:
                logging.error(msg)
                success = False

    return success
