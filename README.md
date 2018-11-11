# DCOS Context Management

## Context anlegen oder loeschen

### Usage
```
./mgt-context.py [--verbose] [--create|delete] [--cluster=DCOS_CLUSTER] [--name=CONTEXT_NAME] [--port_nexus=NEXUS_REPO_PORT] [--cfg_nexus=CFG_FILE_NEXUS] [--cfg_dcos=CFG_FILE_DCOS]
```
### Argumente

* _verbose_       : Verbose Modus                 
* _create_        : DCOS Context anlegen          
* _delete_        : DCOS Context entfernen        
* _name_          : DCOS Context Name             
* _cluster_       : DCOS Cluster Name (siehe --cfg_dcos)
* _port_nexus_    : Port des Nexus Docker Repos   
* _cfg_nexus_     : Optional, Nexus Konfigurationsfile
* _cfg_dcos_      : Optional, DCOS Konfigurationsfile

### Beispiele
#### Anlegen:
```
./mgt-context.py --create --name="demo_context" --port_nexus=50001 --cluster="dcos_tru"
```
#### Loeschen:
```
./mgt-context.py --delete --name="demo_context" --cluster="dcos_tru"
```

## User Gruppe hinzufuegen/entfernen

### Usage
```
./mgt-group.py [--verbose] [--add|remove] [--gid=GROUP_NAME] [--role=ROLE] [--name=CONTEXT_NAME] [--cluster=DCOS_CLUSTER] [--cfg_dcos=CFG_FILE_DCOS]
```

### Argumente
* _verbose_       : Verbose Modus                 
* _add_           : Gruppe hinzufuegen            
* _remove_        : Gruppe entfernen              
* _gid_           : DCOS User Gruppen Name        
* _role_          : Rolle z.B. devops oder dev    
* _name_          : DCOS Service Gruppen name     
* _remove_        : Gruppe entfernen              
* _cluster_       : DCOS Cluster Name (siehe --cfg_dcos)
* _cfg_dcos_      : Optional, DCOS Konfigurationsfile

### Beispiele

#### Anlegen:
```
./mgt-group.py --add --gid="z000-demogruppe" --role="devops" --cluster="dcos_tru"
```
#### Loeschen:
```
  ./mgt-group.py --remove --gid="z000-demogruppe" --role="devops" --cluster="dcos_tru"
```