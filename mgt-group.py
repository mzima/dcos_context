#!/usr/bin/python3

import getopt
import sys
import re
import yaml
import lib.dcos as dcos
import lib.schema as schema
import logging


def usage():
    """ Usage Message """
    print('Usage:\n', sys.argv[0],
          '[--verbose] [--add|remove] [--gid=GROUP_NAME] [--role=ROLE] [--name=CONTEXT_NAME] ' +
          '[--cluster=DCOS_CLUSTER] [--cfg_dcos=CFG_FILE_DCOS]')
    print("\nUser Gruppe zu einem DCOS Context hinzufuegen/entfernen")
    print("\nArguments:")
    print(" %-15s %-30s" % ("--verbose", "Verbose Modus"))
    print(" %-15s %-30s" % ("--add", "Gruppe hinzufuegen"))
    print(" %-15s %-30s" % ("--remove", "Gruppe entfernen"))
    print(" %-15s %-30s" % ("--gid", "DCOS User Gruppen Name"))
    print(" %-15s %-30s" % ("--role", "Rolle z.B. devops oder dev"))
    print(" %-15s %-30s" % ("--name", "DCOS Service Gruppen name"))
    print(" %-15s %-30s" % ("--remove", "Gruppe entfernen"))
    print(" %-15s %-30s" % ("--cluster", "DCOS Cluster Name (siehe --cfg_dcos)"))
    print(" %-15s %-30s" % ("--cfg_dcos", "Optional, DCOS Konfigurationsfile"))
    print("\nExamples:")
    print(" Anlegen:")
    print(" ", sys.argv[0], '--add --gid="z000-demogruppe" --role="devops" --cluster="dcos_tru"')
    print(" Loeschen:")
    print(" ", sys.argv[0], '--remove --gid="z000-demogruppe" --role="devops" --cluster="dcos_tru"')
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
    arg_cfg_dcos = "/tmp/dcos.yml"
    arg_verbose = False
    arg_add = False
    arg_remove = False
    arg_cluster = False
    arg_context_name = False
    arg_role = False
    arg_gid = False

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "",
            ["help", "add", "remove", "cluster=", "name=", "gid=", "role=", "verbose", "cfg_nexus", "cfg_dcos="]
        )
    except getopt.GetoptError as err:
        str(err)
        usage()

    for opt, arg in opts:
        if opt in '--help':
            usage()
        elif opt in '--verbose':
            arg_verbose = True
        elif opt in '--add':
            arg_add = True
        elif opt in '--remove':
            arg_remove = True
        elif opt in '--cluster':
            arg_cluster = arg
        elif opt in '--name':
            arg_context_name = arg
        elif opt in '--role':
            arg_role = arg
        elif opt in '--gid':
            arg_gid = arg
        elif opt in '--cfg_dcos':
            arg_cfg_dcos = arg
        else:
            usage()

    # Argument Parsing
    if not arg_cluster:
        usage()
    elif not arg_context_name:
        usage()
    elif not arg_gid and arg_gid:
        usage()
    elif not arg_role and arg_role:
        usage()
    if (arg_remove and arg_add) or (not arg_remove and not arg_add):
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

    # Configuration File Variables
    dcos_api_url = cfg_dcos[arg_cluster]["url"]
    dcos_api_user = cfg_dcos[arg_cluster]["user"]
    dcos_api_pass = cfg_dcos[arg_cluster]["password"]

    logging.info("Parameter Context-Name: " + arg_context_name)
    logging.info("Parameter Cluster-Name: " + arg_cluster)
    logging.info("Parameter GID: " + arg_gid)

    # Tasks
    rsp = dcos_user_group(
        remove=arg_remove,
        add=arg_add,
        gid=arg_gid,
        role=arg_role,
        context_name=arg_context_name,
        api_user=dcos_api_user,
        api_pass=dcos_api_pass,
        api_url=dcos_api_url
    )

    if not rsp:
        logging.error("Es ist ein Fehler aufgetreten!")
        sys.exit(1)
    else:
        logging.info("Erfolgreich beendet")
        sys.exit(0)


def dcos_user_group(remove, add, gid, role, context_name, api_user, api_pass, api_url):
    """
    DCOS User Gruppe anlegen oder entfernen

    Args:
        remove = User Gruppe entferen (bool)
        add = User Gruppe hinzufuegen (bool)
        gid = User Gruppen Name (string)
        role = Rolle der User Gruppe (string: dev, devops)
        context_name = Name des DCOS Context (string)
        api_user = DCOS API User (string)
        api_pass = DCOS API Passwort (string)
        api_url = DCOS API URL (string)

    Returns:
        True/False (bool)
    """
    success = True
    api_token = dcos.get_token(api_url, api_user, api_pass)
    ba_env = get_ba_env(api_url)

    schema_group = {
        gid: {
            "role": role
        }
    }

    # API Schema ermitteln
    schema_acl = schema.dcos(context_name)["user_group_acl"][ba_env][role]

    if add:
        # Gruppe anlegen
        dcos.create_user_group(schema_group, api_url, api_token)
        dcos.create_user_group_acl(schema_acl, gid, api_url, api_token)
    elif remove:
        # Gruppe loeschen
        dcos.delete_user_group(schema_group, api_url, api_token)
    else:
        logging.error("undefined")

    return success


def get_ba_env(url):
    """
    BA Environment ermitteln

    Args:
        url: URL (string: http://...)

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
