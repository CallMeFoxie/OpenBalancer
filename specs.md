# OpenBalancer REST API reference

**GET /upstream/** - lists all [upstreams](#upstream)  
**POST /upstream/** - creates a new [upstream](#upstream)  
**GET /upstream/&lt;upstream_name&gt;** - lists a specific [upstream](#upstream)  
**PUT /upstream/&lt;upstream_name&gt;** - replaces an [upstream](#upstream)  
**PATCH /upstream/&lt;upstream_name&gt;** - patches an [upstream](#upstream)  
**DELETE /upstream/&lt;upstream_name&gt;** - deletes an empty [upstream](#upstream)  


**GET /check/** - lists all [checks](#checks)  
**POST /check/** - creates a new check  
**GET /check/&lt;check_name&gt;** - lists a specific [check](#checks)  
**PATCH /check/&lt;check_name&gt;** - changes a check  
**PUT /check/&lt;check_name&gt;** - replaces a check  


**GET /upstream/&lt;upstream_name&gt;/node** - lists all nodes in an upstream  
**POST /upstream/&lt;upstream_name&gt;/node** - adds a new node to an upstream  
**PUT /upstream/&lt;upstream_name&gt;/node/&lt;upstream_hostname&gt;** - replaces a node in an upstream  
**PATCH /upstream/&lt;upstream_name&gt;/node/&lt;upstream_hostname&gt;** - patches a node in an upstream  
**DELETE /upstream/&lt;upstream_name&gt;/node/&lt;upstream_hostname&gt;** - deletes a node in an upstream  


**GET /upstream/&lt;upstream_name&gt;/check** - lists all checks for an upstream  
**POST /upstream/&lt;upstream_name&gt;/check** - adds a check to an upstream  
**PUT /upstream/&lt;upstream_name&gt;/check/&lt;check_name&gt;** - replaces a check in an upstream  
**PATCH /upstream/&lt;upstream_name&gt;/check/&lt;check_name&gt;** - patches a check in an upstream  
**DELETE /upstream/&lt;upstream_name&gt;/check/&lt;check_name&gt;** - removes a check from an upstream  


**GET /upstream/&lt;upstream_name&gt;/acl** - lists ACLs for all upstreams  
**POST /upstream/&lt;upstream_name&gt;/acl** - adds a new ACL to an upstream  
**PUT /upstream/&lt;upstream_name&gt;/acl/&lt;group_name&gt;** - replaces ACL for an upstream group  
**PATCH /upstream/&lt;upstream_name&gt;/acl/&lt;group_name&gt;** - patches ACL for an upstream group  
**DELETE /upstream/&lt;upstream_name&gt;/acl/&lt;group_name&gt;** - removes group from an upstream ACL  


**GET /node** - lists all upstreams defined on a node  
**POST /node** - creates a new access node  
**POST /node/&lt;node_hostname&gt;** - adds a new upstream to a node  
**DELETE /node/&lt;node_hostname&gt;/&lt;upstream_name&gt;** - removes an upstream from a node  
**DELETE /node/&lt;node_hostname&gt;** - deletes an access node  


**DELETE /management/node** - safely resets a LOCAL node completely  
**DELETE /management/node?force** - force resets a LOCAL node completely  


**GET /cluster/node** - gets node list and basic settings  
**GET /cluster/node/&lt;host_name&gt;** - gets specific node's settings  
**PUT /cluster/node/&lt;host_name&gt;** - replaces node's settings  
**POST /cluster/node** - adds a new node, see [joining a cluster](#joining)  
**POST /cluster/join** - joins a cluster, see [joining a cluster](#joining)  
**PATCH /cluster/node/&lt;host_name&gt;** - changes a parameter about a node  
**DELETE /cluster/node/&lt;host_name&gt;** - disconnects a node from the current cluster  


**GET /user** - gets users + their group membership  
**GET /user/&lt;user_name&gt;** - gets a specific user  
**POST /user** - adds a new user  
**DELETE /user/&lt;user_name&gt;** - deletes a user  
**PATCH /user/&lt;user_name&gt;** - changes a parameter about a user  
**POST /user/&lt;user_name&gt;/group** - adds a user to a group  
**DELETE /user/&lt;user_name&gt;/group/&lt;group_name&gt;** - deletes a user from a group  


**GET /group** - gets all groups and their ACLs  
**GET /group/&lt;group_name&gt;** - gets a specific group and its ACL  
**POST /group** - add a group  
**DELETE /group/&lt;group_name&gt;** - deletes a specific group  
**PATCH /group/&lt;group_name&gt;** - replaces group's settings  


**POST /auth** - auths a user  
**DELETE /auth** - deauths a user  


**GET /status** - shows status  


*UNIQUE items cannot be patched/changed once created*  


Users do not have any permissions, groups are always required!  
Groups have automatic WRITE access to their upstreams and checks.  
Groups without GLOBAL_RO cannot re-use checks of other teams.  
All requests except POST /auth/ require X-Auth-Token header with auth token retrieved via /auth/  
Default login is root:root, with group admins, which has full permissions.  
Admins group cannot be modified nor deleted, just as root user can never lose admins group membership.  


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
  - **group** - user's group membership (used for global flags)
  - **groups** - user's secondary group membership (used for upstream membership)
  - **enabled** - user is enabled (true/false) to authenticate

## group
  - **group_name** - unique group name
  - **global_permissions** - (MANAGEMENT | SUPER | GLOBAL_RO | GLOBAL_RW) flags array:
    - **MANAGEMENT** - user can manage users and groups, cannot change GLOBAL* flags unless has GLOBAL_RW flag
    - **SUPER** - super user can also manage controllers
    - **GLOBAL_RO** - user can view any group's upstream
    - **GLOBAL_RW** - user can change any group's upstream and change GLOBAL* flags for groups
    - **CERT_MNG** - user can create and download peer certificates
    - **CERT_NODE** - user can create and download client certificates
  
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
if there was no-one logged yet, the default login is root:root  
  
## auth process reply if success
  - **token**
  - **token_expiration**
  
## joining
1st stage, sent to the cluster/node:
  - **hostname** - new node's hostname (must not be in the cluster already)
reply:
  - **token** - temporary token that has request peer certificate permission, has short lived 
  - **expiration** - seconds when the token and join request expires
  - **nodes** - nodes of the cluster to join on
  
2nd stage, sent to the new node cluster/join:
  - **password** - remote root's password
  - **nodes** - cluster nodes to join (requires one as they sync, but the more the better)
  - **token** - temporary token to request certificates with
  
This message does not use username as it is required to be root login (can be completely wiped/freshly installed node).  
Joining a cluster means resetting current node and wiping all of the local configuration except local root's password and HTTPS certificates.  
A message is sent with the cluster/origin node settings so that the new server knows where to connect to.  
New server afterwards changes local ETCD cluster node list, clears local ETCD data, requests a new peer certificate using temporary token from existing cluster, downloads it, replaces old ones (if exist).  