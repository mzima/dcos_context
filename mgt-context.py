#!/usr/bin/python3

import getopt
import sys
import re
import yaml
import lib.nexus as nexus
import lib.dcos as dcos
import lib.schema as schema
import logging


def usage():
    """ Usage Message """
    print('Usage: ', sys.argv[0],
          '[--verbose] [--create|delete] [--cluster=DCOS_CLUSTER] [--name=CONTEXT_NAME] ' +
          '[--port_nexus=NEXUS_REPO_PORT] [--cfg_nexus=CFG_FILE_NEXUS] [--cfg_dcos=CFG_FILE_DCOS]')
    print("\nDCOS Context anlegen oder loeschen")
    print("\nArguments:")
    print(" %-15s %-30s" % ("--verbose", "Verbose Modus"))
    print(" %-15s %-30s" % ("--create", "DCOS Context anlegen"))
    print(" %-15s %-30s" % ("--delete", "DCOS Context entfernen"))
    print(" %-15s %-30s" % ("--name", "DCOS Context Name"))
    print(" %-15s %-30s" % ("--cluster", "DCOS Cluster Name (siehe --cfg_dcos)"))
    print(" %-15s %-30s" % ("--port_nexus", "Port des Nexus Docker Repos"))
    print(" %-15s %-30s" % ("--cfg_nexus", "Optional, Nexus Konfigurationsfile"))
    print(" %-15s %-30s" % ("--cfg_dcos", "Optional, DCOS Konfigurationsfile"))
    print("\nExamples:")
    print(" Anlegen:")
    print(" ", sys.argv[0], '--create --name="demo_context" --port_nexus=50001 --cluster="dcos_tru"')
    print(" Loeschen:")
    print(" ", sys.argv[0], '--delete --name="demo_context" --cluster="dcos_tru"')
    print("\n")
    sys.exit(2)


def main():
    """
    MAIN

    Args:
        cfg = Konfigurationsfiles fuer Nexus und DCOS (dict)

    Returns:
        True/False
    """

    # Argument Handling
    arg_cfg_dcos = '/tmp/con.yml'
    arg_cfg_nexus = '/tmp/nexus.yml'
    arg_verbose = False
    arg_create = False
    arg_delete = False
    arg_cluster = False
    arg_context_name = False
    arg_port_nexus = False

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "",
            ["help", "create", "delete", "cluster=", "name=", "port_nexus=", "verbose", "cfg_nexus=", "cfg_dcos="]
        )
    except getopt.GetoptError as err:
        str(err)
        usage()

    for opt, arg in opts:
        if opt in '--help':
            usage()
        elif opt in '--verbose':
            arg_verbose = True
        elif opt in '--create':
            arg_create = True
        elif opt in '--delete':
            arg_delete = True
        elif opt in '--cluster':
            arg_cluster = arg
        elif opt in '--name':
            arg_context_name = arg
        elif opt in '--port_nexus':
            arg_port_nexus = arg
        elif opt in '--cfg_nexus':
            arg_cfg_nexus = arg
        elif opt in '--cfg_dcos':
            arg_cfg_dcos = arg
        else:
            usage()

    # Argument Parsing
    if not arg_cluster:
        usage()
    elif not arg_context_name:
        usage()
    elif not arg_port_nexus and arg_create:
        usage()

    if (arg_create and arg_delete) or (not arg_create and not arg_delete):
        usage()

    # Logging
    if arg_verbose:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s : %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    else:
        logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARN)
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(levelname)s : %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    # Configuration Files
    with open(arg_cfg_dcos, 'r') as ymldcos:
        cfg_dcos = yaml.load(ymldcos)

    with open(arg_cfg_nexus, 'r') as ymlnexus:
        cfg_nexus = yaml.load(ymlnexus)

    # Configuration File Variables
    dcos_url = cfg_dcos[arg_cluster]["url"]
    dcos_api_user = cfg_dcos[arg_cluster]["user"]
    dcos_api_pass = cfg_dcos[arg_cluster]["password"]
    nexus_url = cfg_nexus[arg_cluster]["url"]
    nexus_docker_port = arg_port_nexus
    nexus_api_user = cfg_nexus[arg_cluster]["user"]
    nexus_api_pass = cfg_nexus[arg_cluster]["password"]

    logging.info("Parameter Context-Name: " + arg_context_name)
    logging.info("Parameter Cluster-Name: " + arg_cluster)
    logging.info("Parameter Nexus-Port: " + arg_port_nexus)

    # Tasks
    nexus_rsp = nexus_tasks(
        param=schema.nexus(arg_context_name, nexus_docker_port),
        create=arg_create,
        delete=arg_delete,
        api_url=nexus_url,
        api_user=nexus_api_user,
        api_pass=nexus_api_pass
    )

    dcos_rsp = dcos_tasks(
        param=schema.dcos(arg_context_name),
        create=arg_create,
        delete=arg_delete,
        api_url=dcos_url,
        api_user=dcos_api_user,
        api_pass=dcos_api_pass
    )

    if not nexus_rsp or not dcos_rsp:
        logging.error("Es ist ein Fehler aufgetreten!")
        sys.exit(1)
    else:
        logging.info("Erfolgreich beendet")
        sys.exit(0)


def nexus_tasks(param, create, delete, api_url, api_user, api_pass):
    """
    NEXUS Tasks realisieren

    Args:
        param: REST Call Schema (dict: siehe schema.py)
        create: Nexus Objekt anlegen (bool)
        delete: Nexus Objekt loeschen (bool)
        api_url: Nexus URL (string)
        api_user: Nexus User (string)
        api_pass: Nexus Passwort (string)

    Returns:
        True/False
    """
    success = True
    if create:
        # Context anlegen
        for url in api_url:
            if not nexus.create_repo(param=param["repo"], user=api_user, password=api_pass, url=url):
                success = False
            if not nexus.create_role(param=param["role"], user=api_user, password=api_pass, url=url):
                success = False
            if not nexus.create_user(users=param["user"], user=api_user, password=api_pass, url=url):
                success = False

    elif delete:
        # Context loeschen
        for url in api_url:
            if not nexus.delete_repo(param=param["repo"], user=api_user, password=api_pass, url=url):
                success = False
            if not nexus.delete_role(param=param["role"], user=api_user, password=api_pass, url=url):
                success = False
            if not nexus.delete_user(users=param["user"], user=api_user, password=api_pass, url=url):
                success = False

    return success


def dcos_tasks(param, create, delete, api_url, api_user, api_pass):
    """
    DCOS Tasks realisiseren

    Args:
        param: REST Call Schema (dict: siehe schema.py)
        create: DCOS Objekt anlegen (bool)
        delete: DCOS Objekt loeschen (bool)
        api_url: DCOS URL (string)
        api_user: DCOS User (string)
        api_pass: DCOS Passwort (string)

    Returns:
        True/False
    """
    success = True
    token = dcos.get_token(url=api_url, user=api_user, password=api_pass)
    ba_env = get_ba_env(url=api_url)

    if create:
        # Context anlegen
        if not dcos.create_service_group(param=param["service_group"], url=api_url, token=token):
            success = False
        if not dcos.create_user_group(param=param["user_group"], url=api_url, token=token):
            success = False
        for group in param["user_group"]:
            group_role = param["user_group"][group]["role"]
            if not dcos.create_user_group_acl(
                    param=param["user_group_acl"][ba_env][group_role],
                    gid=group, url=api_url,
                    token=token):
                success = False
    elif delete:
        # Context loeschen
        if not dcos.delete_service_group(param=param["service_group"]["id"], url=api_url, token=token):
            success = False
        if not dcos.delete_user_group(param=param["user_group"], url=api_url, token=token):
            success = False

    return success


def get_ba_env(url):
    """
    BA Environment ermitteln

    Args:
        url: URL (string)

    Returns:
        prod, nprod
    """
    if re.match(r".+[eis]dst\.[eis]baintern\.de.*", url) \
            or re.match(r".+iirzi\.de.*", url):
        ba_env = "nprod"
    else:
        ba_env = "prod"

    return ba_env


if __name__ == "__main__":
    main()

