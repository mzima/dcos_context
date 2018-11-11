#
# Params
#


def nexus(name, docker_port):
    """
    Schema fuer Nexus

    Args:
        name = Context Name
        docker_port = Portnummer fuer das Nexus Docker Repo

    Returns:
        API Schema (dict)
    """
    schema = {
        # User Schema
        "user": {
            name + "_dev": {
                "role": [name + "-dev"]
            },
            name + "_devops": {
                "role": [name + "-devops"]
            }
        },
        # Repository Schema
        "repo": {
            name: {
                "type": "docker",
                "port": docker_port
            },
            name + "-raw": {
                "type": "raw"
            }
        },
        # Rollen ACLs
        "role": {
            name + "-dev": {
                "privileges": [
                    "nx-repository-view-docker-" + name + "-browse",
                    "nx-repository-view-docker-" + name + "-read",
                    "nx-repository-view-raw-" + name + "-raw-browse",
                    "nx-repository-view-raw-" + name + "-raw-read"
                ],
                "contained_roles": []
            },
            name + "-devops": {
                "privileges": [
                    "nx-repository-admin-docker-" + name + "-*",
                    "nx-repository-admin-raw-" + name + "-raw-*",
                    "nx-repository-view-docker-" + name + "-*",
                    "nx-repository-view-raw-" + name + "-raw-*"
                ],
                "contained_roles": [name + "-dev"]
            }
        }
    }
    return schema


def dcos(name):
    """
    Schema fuer DCOS

    Args:
        name = Context Name

    Returns:
        API Schema (dict)
    """
    schema = {
        # Service Group
        "service_group": {
            "id": "/" + name,
            "groups": [
                {"id": "/" + name + "/dev"},
                {"id": "/" + name + "/lpt"},
                {"id": "/" + name + "/pen"},
                {"id": "/" + name + "/rc"},
                {"id": "/" + name + "/scrub"},
                {"id": "/" + name + "/uat"},
            ]
        },
        # User Group
        "user_group": {
            "dev_" + name: {
                "role": "dev"
            },
            "devops_" + name: {
                "role": "devops"
            }
        },
        # User Group ACL
        "user_group_acl": {
            "prod": {
                "dev": {
                    "dcos:adminrouter:ops:historyservice": ["full"],
                    "dcos:adminrouter:ops:mesos": ["full"],
                    "dcos:adminrouter:ops:networking": ["full"],
                    "dcos:adminrouter:ops:slave": ["full"],
                    "dcos:adminrouter:ops:system-health": ["full"],
                    "dcos:adminrouter:service:marathon": ["full"],
                    "dcos:adminrouter:service:metronome": ["full"],
                    "dcos:mesos:agent:executor:app_id:/" + name: ["read"],
                    "dcos:mesos:agent:framework:role:slave_public": ["read"],
                    "dcos:mesos:agent:sandbox:app_id:/" + name: ["read"],
                    "dcos:mesos:agent:task:app_id:/" + name: ["read"],
                    "dcos:mesos:master:executor:app_id:/" + name: ["read"],
                    "dcos:mesos:master:framework:role:slave_public": ["read"],
                    "dcos:mesos:master:task:app_id:/" + name: ["read"],
                    "dcos:secrets:default:/" + name: ["read"],
                    "dcos:service:marathon:marathon:services:/" + name: ["read"],
                    "dcos:service:metronome:metronome:jobs:/" + name: ["read"]
                },
                "devops": {
                    "dcos:adminrouter:ops:historyservice": ["full"],
                    "dcos:adminrouter:ops:mesos": ["full"],
                    "dcos:adminrouter:ops:metadata": ["full"],
                    "dcos:adminrouter:ops:networking": ["full"],
                    "dcos:adminrouter:package": ["full"],
                    "dcos:adminrouter:ops:slave": ["full"],
                    "dcos:adminrouter:ops:system-health": ["full"],
                    "dcos:adminrouter:secrets": ["full"],
                    "dcos:adminrouter:service:marathon": ["full"],
                    "dcos:adminrouter:service:metronome": ["full"],
                    "dcos:mesos:agent:endpoint:path:/monitor/statistics": ["read"],
                    "dcos:mesos:agent:executor:app_id:" + name: ["read"],
                    "dcos:mesos:agent:flags": ["read"],
                    "dcos:mesos:agent:framework:role:*": ["read"],
                    "dcos:mesos:agent:framework:role:slave_public": ["read"],
                    "dcos:mesos:agent:log": ["read"],
                    "dcos:mesos:agent:sandbox:app_id:/" + name: ["read"],
                    "dcos:mesos:agent:task:app_id:/" + name: ["read"],
                    "dcos:mesos:master:endpoint:path": ["read"],
                    "dcos:mesos:master:executor:app_id:/" + name: ["read"],
                    "dcos:mesos:master:framework:role:*": ["read"],
                    "dcos:mesos:master:framework:role:slave_public": ["read"],
                    "dcos:mesos:master:log": ["read"],
                    "dcos:mesos:master:task:app_id:/infosysbub": ["read"],
                    "dcos:secrets:list:default:/": ["read"],
                    "dcos:service:metronome:metronome:jobs:/" + name: ["read"],
                    "dcos:service:metronome:metronome:jobs:/" + name + "/preprod": ["create", "delete", "read",
                                                                                    "update"],
                    "dcos:service:metronome:metronome:jobs:/" + name + "/prod": ["create", "delete", "read", "update"],
                    "dcos:service:marathon:marathon:services:/" + name: ["read"],
                    "dcos:service:marathon:marathon:services:/" + name + "infosysbub/preprod": ["create", "delete",
                                                                                                "read", "update"],
                    "dcos:service:marathon:marathon:services:/" + name + "/prod": ["create", "delete", "read", "update"]
                }
            },
            "nprod": {
                "dev": {
                    "dcos:adminrouter:ops:historyservice": ["full"],
                    "dcos:adminrouter:ops:mesos": ["full"],
                    "dcos:adminrouter:ops:metadata": ["full"],
                    "dcos:adminrouter:ops:networking": ["full"],
                    "dcos:adminrouter:ops:slave": ["full"],
                    "dcos:adminrouter:ops:system-health": ["full"],
                    "dcos:adminrouter:service:marathon": ["full"],
                    "dcos:adminrouter:service:metronome": ["full"],
                    "dcos:mesos:agent:executor:app_id:/" + name: ["read"],
                    "dcos:mesos:agent:framework:role:slave_public": ["read"],
                    "dcos:mesos:agent:sandbox:app_id:/" + name: ["read"],
                    "dcos:mesos:agent:sandbox:app_id:/" + name + "/dev": ["read"],
                    "dcos:mesos:agent:sandbox:app_id:/" + name + "/lpt": ["read"],
                    "dcos:mesos:agent:sandbox:app_id:/" + name + "/pen": ["read"],
                    "dcos:mesos:agent:sandbox:app_id:/" + name + "/rc": ["read"],
                    "dcos:mesos:agent:sandbox:app_id:/" + name + "/scrub": ["read"],
                    "dcos:mesos:agent:sandbox:app_id:/" + name + "/uat": ["read"],
                    "dcos:mesos:agent:task:app_id:/" + name: ["read"],
                    "dcos:mesos:master:executor:app_id:/" + name: ["read"],
                    "dcos:mesos:master:framework:role:slave_public": ["read"],
                    "dcos:mesos:master:task:app_id:/" + name: ["read"],
                    "dcos:secrets:default:/" + name + "/dev": ["create", "delete", "read", "update"],
                    "dcos:secrets:default:/" + name + "/scrub": ["create", "delete", "read", "update"],
                    "dcos:service:marathon:marathon:services:/" + name + "/dev": ["create", "delete", "read", "update"],
                    "dcos:service:marathon:marathon:services:/" + name + "/lpt": ["read"],
                    "dcos:service:marathon:marathon:services:/" + name + "/pen": ["read"],
                    "dcos:service:marathon:marathon:services:/" + name + "/rc": ["read"],
                    "dcos:service:marathon:marathon:services:/" + name + "/scrub": ["create", "delete", "read", "update"],
                    "dcos:service:marathon:marathon:services:/" + name + "/uat": ["read"],
                    "dcos:service:metronome:metronome:jobs:/" + name + "/dev": ["create", "delete", "read", "update"],
                    "dcos:service:metronome:metronome:jobs:/" + name + "/lpt": ["read"],
                    "dcos:service:metronome:metronome:jobs:/" + name + "/pen": ["read"],
                    "dcos:service:metronome:metronome:jobs:/" + name + "/rc": ["read"],
                    "dcos:service:metronome:metronome:jobs:/" + name + "/scrub": ["create", "delete", "read", "update"],
                    "dcos:service:metronome:metronome:jobs:/" + name + "/uat": ["read"]
                },
                "devops": {
                    "dcos:adminrouter:ops:historyservice": ["full"],
                    "dcos:adminrouter:ops:mesos": ["full"],
                    "dcos:adminrouter:ops:metadata": ["full"],
                    "dcos:adminrouter:ops:networking": ["full"],
                    "dcos:adminrouter:package": ["full"],
                    "dcos:adminrouter:ops:slave": ["full"],
                    "dcos:adminrouter:ops:system-health": ["full"],
                    "dcos:adminrouter:secrets": ["full"],
                    "dcos:adminrouter:service:marathon": ["full"],
                    "dcos:adminrouter:service:metronome": ["full"],
                    "dcos:mesos:agent:endpoint:path:/monitor/statistics": ["read"],
                    "dcos:mesos:agent:executor:app_id:/" + name + "": ["read"],
                    "dcos:mesos:agent:flags": ["read"],
                    "dcos:mesos:agent:framework:role:*": ["read"],
                    "dcos:mesos:agent:framework:role:slave_public": ["read"],
                    "dcos:mesos:agent:log": ["read"],
                    "dcos:mesos:agent:sandbox:app_id:/" + name + "": ["read"],
                    "dcos:mesos:agent:task:app_id:/" + name + "": ["read"],
                    "dcos:mesos:master:endpoint:path": ["read"],
                    "dcos:mesos:master:executor:app_id:/" + name + "": ["read"],
                    "dcos:mesos:master:framework:role:*": ["read"],
                    "dcos:mesos:master:framework:role:slave_public": ["read"],
                    "dcos:mesos:master:log": ["read"],
                    "dcos:mesos:master:task:app_id:/" + name + "": ["read"],
                    "dcos:secrets:list:default:/": ["read"],
                    "dcos:service:metronome:metronome:jobs:/" + name + "": ["read"],
                    "dcos:service:metronome:metronome:jobs:/" + name + "/uat": ["create", "delete", "read", "update"],
                    "dcos:service:metronome:metronome:jobs:/" + name + "/scrub": ["create", "delete", "read", "update"],
                    "dcos:service:metronome:metronome:jobs:/" + name + "/rc": ["create", "delete", "read", "update"],
                    "dcos:service:metronome:metronome:jobs:/" + name + "/pen": ["create", "delete", "read", "update"],
                    "dcos:service:metronome:metronome:jobs:/" + name + "/lpt": ["create", "delete", "read", "update"],
                    "dcos:service:metronome:metronome:jobs:/" + name + "/dev": ["create", "delete", "read", "update"],
                    "dcos:service:marathon:marathon:services:/" + name + "": ["read"],
                    "dcos:service:marathon:marathon:services:/" + name + "/uat": ["create", "delete", "read", "update"],
                    "dcos:service:marathon:marathon:services:/" + name + "/scrub": ["create", "delete", "read", "update"],
                    "dcos:service:marathon:marathon:services:/" + name + "/rc": ["create", "delete", "read", "update"],
                    "dcos:service:marathon:marathon:services:/" + name + "/pen": ["create", "delete", "read", "update"],
                    "dcos:service:marathon:marathon:services:/" + name + "/lpt": ["create", "delete", "read", "update"],
                    "dcos:service:marathon:marathon:services:/" + name + "/dev": ["create", "delete", "read", "update"]
                }
            }
        }
    }
    return schema
