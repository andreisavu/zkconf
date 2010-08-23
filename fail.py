#! /usr/bin/env python
""" Make node from a local ZooKeeper cluster fail """

import sys
import os
import re
import optparse
import random
import time
import signal

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    parser = optparse.OptionParser()
    parser.add_option('-l', '--leader', action='store_true', default=False,
        help='Only kill the current leader of the cluster')
    opts, args = parser.parse_args()

    nodes = get_nodes()
    
    while True:
        n = random.choice(nodes)
        kill_node(n)
        start_node(n)
        wait_join_cluster(n)
        time.sleep(1)

def kill_node(n):
    p = os.path.join(CURRENT_DIR, "%s:%s" % n, 'zookeeper_server.pid')
    if not os.path.exists(p):
        return False

    pid = int(open(p).read())
    print 'killing %s running with pid %d ...' % (n, pid)
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        print 'process with pid %d not found.' % pid

def start_node(n):
    print 're-starting the node %s ...' % (n,)
    

def wait_join_cluster(n):
    print 'waiting for node to join the cluster ...'

def get_nodes():
    nodes = []
    for f in os.listdir(CURRENT_DIR):
        if os.path.isdir(f):
            m = re.match('^(\w+?):(\d+)$', f)
            if m is not None:
                nodes.append(m.group(1,2))
    return nodes

if __name__ == '__main__':
    sys.exit(main())

