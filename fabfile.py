from __future__ import with_statement
import os
from fabric.api import *
from local_fabfile import LOCAL_CODE_ROOT


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
    for directory in ['.']:
        cd_path = os.path.join(LOCAL_CODE_ROOT, directory)
        local('cd %s && git add --all && git commit && git push origin master' % cd_path)