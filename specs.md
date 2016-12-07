# OpenBalancer REST API reference

**GET /upstream/** - lists all [upstreams](#upstream)

**POST /upstream/** - creates a new [upstream](#upstream)

**GET /upstream/<upstream_name>** - lists a specific [upstream](#upstream)

**PUT /upstream/<upstream_name>** - replaces an [upstream](#upstream)

**PATCH /upstream/<upstream_name>** - patches an [upstream](#upstream)

**DELETE /upstream/<upstream_name>** - deletes an empty [upstream](#upstream)




**GET /check/** - lists all [checks](#checks)

**POST /check/** - creates a new check

**GET /check/<check_name>** - lists a specific [check](#checks)

**PATCH /check/<check_name>** - changes a check

**PUT /check/<check_name>** - replaces a check




**GET /upstream/<upstream_name>/node** - lists all nodes in an upstream

**POST /upstream/<upstream_name>/node** - adds a new node to an upstream

**PUT /upstream/<upstream_name>/node/<upstream_hostname>** - replaces a node in an upstream

**PATCH /upstream/<upstream_name>/node/<upstream_hostname>** - patches a node in an upstream

**DELETE /upstream/<upstream_name>/node/<upstream_hostname>** - deletes a node in an upstream




**GET /upstream/<upstream_name>/check** - lists all checks for an upstream

**POST /upstream/<upstream_name>/check** - adds a check to an upstream

**PUT /upstream/<upstream_name>/check/<check_name>** - replaces a check in an upstream

**PATCH /upstream/<upstream_name>/check/<check_name>** - patches a check in an upstream

**DELETE /upstream/<upstream_name>/check/<check_name>** - removes a check from an upstream




**GET /upstream/<upstream_name>/acl** - lists ACLs for all upstreams

**POST /upstream/<upstream_name>/acl** - adds a new ACL to an upstream

**PUT /upstream/<upstream_name>/acl/<group_name>** - replaces ACL for an upstream group

**PATCH /upstream/<upstream_name>/acl/<group_name>** - patches ACL for an upstream group

**DELETE /upstream/<upstream_name>/acl/<group_name>** - removes group from an upstream ACL




**GET /node** - lists all upstreams defined on a node

**POST /node** - creates a new access node

**POST /node/<node_hostname>** - adds a new upstream to a node

**DELETE /node/<node_hostname>/<upstream_name>** - removes an upstream from a node

**DELETE /node/<node_hostname>** - deletes an access node




**GET /management/node** - gets node list and basic settings

**POST /management/node/** - adds a new node

**GET /management/node/<host_name>** - gets specific node's settings

**PUT /management/node/<host_name>** - replaces node's settings

**PATCH /management/node/<host_name>** - changes a parameter about a node

**DELETE /management/node/<host_name>** - disconnects a node from the current cluster

**DELETE /management/node** - safely resets a LOCAL node completely

**DELETE /management/node?force** - force resets a LOCAL node completely




**GET /user** - gets users + their group membership

**GET /user/<user_name>** - gets a specific user

**POST /user** - adds a new user

**DELETE /user/<user_name>** - deletes a user

**PATCH /user/<user_name>** - changes a parameter about a user

**POST /user/<user_name>** - adds a user to a group

**DELETE /user/<user_name>/<group_name>** - deletes a user from a group




**GET /group** - gets all groups and their ACLs

**GET /group/<group_name>** - gets a specific group and its ACL

**POST /group** - add a group

**DELETE /group/<group_name>** - deletes a specific group

**PATCH /group/<group_name>** - replaces group's settings




**POST /auth** - auths a user

**DELETE /auth** - deauths a user




**GET /status** - shows status




*UNIQUE items cannot be patched/changed once created*



Users do not have any permissions, groups are always required!

Groups have automatic WRITE access to their upstreams and checks.

Groups without GLOBAL_RO cannot re-use checks of other teams.

All requests except POST /auth/ require X-Auth-Token header with auth token retrieved via /auth/


## upstream
  - **name** - unique name
  - **min_servers** - minimum amount of servers to enable
  - **owner** - group that owns this upstream
  
## checks
  - **name** - unique id
  - **string** - extra string, check specific
  - **base_check** - check which it is based on (can be only base checks)
  - **type** - base/custom (base = programmed in python, HAS to be extended)
  - **owner** - group that owns this check
  
## upstream_hostname
  * **hostname** - unique node name per upstream
  * **weight**
  * **max_fails**
  * **fail_timeout**
  * **force_status** - force status (u)p/(d)own/(n)ormal
  * **failover** - order in which they will be allowed in case of failures (same values will be sorted by alphabet)

  - **resolved_ip** - resolved IP (read-only field)
  
## node
  - **host_name** - unique hostname with port to listen on
  - **description**
  - **owner** - group that owns this node
  
## status
  - **master_node** - node which is running and updating statuses based on checks
  - **etcd_health** - health of the ETCD cluster
  
## management
  - **host_name** - unique hostname 
  - **description**
  
## user
  - **user_name** - unique username (login)
  - **password** - sha1 salted password
  - **salt** - salt used for this password
  - **name** - user's name
  - **group** - user's group membership
  - **enabled** - user is enabled (true/false) to authenticate

## group
  - **group_name** - unique group name
  - **global_permissions** - (MANAGEMENT | SUPER | GLOBAL_RO | GLOBAL_RW) flags array:
    - **MANAGEMENT** - user can manage users and groups, cannot change GLOBAL* flags unless has GLOBAL_RW flag
    - **SUPER** - super user can also manage controllers
    - **GLOBAL_RO** - user can view any group's upstream
    - **GLOBAL_RW** - user can change any group's upstream and change GLOBAL* flags for groups
  
## acl
  - **group_name** - group name to change access of
  - **rule** - WRITE/READ/DENY
  
## auth
  - **user_name** - username to login with
  - **password** - sha1 hashed password
  or
  - **token** - token to delete or re-auth
  
see auth_process
DELETE method to logout and remove token from active tokens, MANAGEMENT can remove any token to force logout anybody
  
## auth process reply if success
  - **token**
  - **token_expiration**