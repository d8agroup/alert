from __future__ import with_statement
import os
from fabric.api import *
from local_fabfile import *


packages = {
    'apt-get': [
        'postgresql',
        'python-psycopg2'
    ]
}


def git():
    for directory in ['django_odc', '.']:
        cd_path = os.path.join(LOCAL_CODE_ROOT, directory)
        local('cd %s && git add --all && git commit && git push origin master' % cd_path)


def recycle():
    run("service apache2 restart")


def deploy(alert_branch='master', odc_branch='master'):
    with cd('/usr/local/metaLayer-alert'):
        run("git fetch")
        run("git merge origin/%s" % alert_branch)
        run("git submodule update")
        run("git status")
    with cd('/usr/local/metaLayer-alert'):
        run("python manage.py collectstatic --noinput")
        run("pip install -r requirements.txt")
    with settings(warn_only=True):
        run("service apache2 restart")
