#!/usr/bin/python3

import sys, os, pprint, requests, configparser, hashlib, logger

### fixed conf stuff
RESTPORT = os.environ('RESTPORT')

TESTPWDROOT = os.environ('TESTPWDROOT')
TESTPWDUSER = os.environ('TESTPWDUSER')
TESTUSER = os.environ('TESTUSER')
MASTERS = os.environ('MASTERS').split(',')
NODES = os.environ('NODES').split(',')
CLIENTS = os.environ('CLIENTS').split(',')

TESTSERVERS = os.environ('TESTSERVERS').split(',')
TESTUPSTERAMS = os.environ('TESTUPSTREAMS').split(',')


### auth stuff
token = ''

def pwd(pwd) {
    s = hashlib.sha1()
    s.update(pwd)
    return s.hexdigest()
}

def req(node, url, method='get', data='', allow_codes={200, 201}, auth_token=None) {
    global token, RESTPORT
    
    print(">   req: {} {}/{}, token: {}".format(method.upper(), node, url, token))
    
    if auth_token == None:
        auth_token = token
    
    
    r = requests.request(method.upper(), "https://{}:{}/{}".format(node, RESTPORT, url), data=data, headers={'X-Auth-Token': auth_token})
    assert r.status_code in allow_codes
    
    return r
}

def auth(node, user, pwd) {
    r = req(node, "auth", "post", '{"username": "{}", "password": "{}"}'.format(user, pwd))
    
    return r.json()['token']
}

def deauth(node, token) {
    print(">   deauth token {}".format(token))
    r = req(node, "auth", "delete", '{"token": "{}"}'.format(token))
}

### master node stuff

def setup_single_master_node(node) {
    global token 
    
    print("> setup single node {}".format(node))
    print(">  authing with default account")
    token = auth(node, "root", pwd("root"))
    
    print(">  changing password")
    req(node, "user/root", "patch", '{"password": "{}"}'.format(pwd(TESTPWDROOT)))
    print(">  logging out and logging back in")
    deauth(node, token)
    token = auth(node, "root", pwd(TESTPWDROOT))
    print("> done")
}

def reset_master_node(node) {
    global token
    print("> reset node {}".format(node))
    req(node, "management/node", "delete")
    token = ''
    print("> done")
}

def join_cluster(cluster, node) {
    print("> joining cluster {} with node {}".format(cluster, node))
    print(">  informing cluster of the new node and getting a new token")
    cl = req(cluster, "cluster/node", "post", '{"hostname": "{}"}'.format(node)).json()
    print(">  informing node to join the cluster, token: {}".format(cl['token']))
    req(node, "cluster/join", "post", json.dumps({'password': TESTPWDROOT, 'nodes': cl['nodes'], 'token': cl['token']}))
    
    print(">  checking cluster access to the new node")
    cluster_token = auth(cluster, "root", pwd(TESTPWDROOT))
    req(cluster, "management/node/{}".format(node), auth_token = cluster_token)
    print("> done")
}

def add_user(cluster, user, xpwd, name, group, groups = {}, enabled = True) {
    print("> adding user {} into the cluster".format(user))
    req(cluster, "user", "post", json.dumps({'user_name': user, 'password': pwd(xpwd), 'name': name, 'group': group, 'groups': groups, 'enabled': enabled}))
    print("> done")
}

### access node stuff


def do_test() {
    print("> setting up all master nodes")
    for master in MASTERS:
        setup_single_master_node(master)
    
    print("> joining them into cluster")
    for i in range(1, MASTERS.len()):
        join_cluster(MASTERS[0], MASTERS[i])
    
    print("> adding a test user")
    add_user(MASTERS[0], TESTUSER, TESTPWDUSER, 'test_user', {'admins'})
    
    print("> logging in with the test user")
    auth(MASTERS[0], TESTUSER, TESTPWDUSER)
    
    print("> setting up upstreams #TODO")
    print("> setting up access nodes #TODO")
    print("> adding upstreams to access nodes #TODO")
    print("> checking access nodes for forwarding to test servers #TODO")
}

if __name__ == "__main__":
    do_test()