from fabric.api import task
from fabric.api import cd
from fabric.api import env
from fabric.api import prefix
from fabric.api import sudo
from fabric.api import run

env.user = ''
env.hosts = ['']

@task(alias="deploy")
def deploy():
    with cd(''):
        run('git pull')
        run('pipenv run pip install -r requirements.txt')
        run('pipenv run python manage.py migrate')

    sudo('systemctl restart blog')
    sudo('systemctl restart nginx')