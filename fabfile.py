from __future__ import with_statement
import os
from fabric.api import *
import time
from local_fabfile import *


packages = {
    'apt-get': [
        'postgresql',
        'python-psycopg2'
    ]
}


def _update_deployment_timestamp():
    import fileinput
    for line in fileinput.input('themes/settings.py', inplace=1):
        if line.startswith('DEPLOYMENT_TIMESTAMP'):
            print 'DEPLOYMENT_TIMESTAMP = %i \n' % int(time.time()),
        else:
            print line,


def git():
    for directory in ['django_odc', '.']:
        cd_path = os.path.join(LOCAL_CODE_ROOT, directory)
        with settings(warn_only=True):
            local('cd %s && git add --all && git commit && git push origin master' % cd_path)


def pull():
    local('cd ~/code/metaLayer/alert/django_odc && git fetch && git merge origin/master')
    local('cd ~/code/metaLayer/alert && git fetch && git merge origin/master')


def manage(command):
    with cd('/usr/local/metaLayer-alert'):
        run("python manage.py %s" % command)


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
