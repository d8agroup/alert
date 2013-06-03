from __future__ import with_statement
import os
from fabric.api import *


packages = {
    'apt-get': [
        'python-mysqldb'
    ],
    'pip': [
        'django=1.5.1',
        'South==0.8.1'
    ]
}


def git():
    for dir in ['/.']:
        local('cd ~/code/metaLayer/alert%s && git add --all && git commit && git push origin master' % dir)