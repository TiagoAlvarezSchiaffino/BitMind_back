from fabric.api import task
from fabric.api import cd
from fabric.api import env
from fabric.api import prefix
from fabric.api import sudo
from fabric.api import run
from fabric.api import get

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

@task(alias='get-log')
def download_error_log():
    sudo ('tail -n 20 /var/log/nginx/error.log.1 > tmp.log')

    get(
        local_path="/home/Programacion/BitMind_back/error_log.log",
        remote_path="/home/tmp.log"
    )

    sudo ('rm tmp.log')