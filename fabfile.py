import random
import os
from fabric import Connection, Config
from patchwork.files import exists, append
from invoke import task


REPO_URL = 'https://github.com/mrnitrate/TOMIS_nptadwords'
site_folder = '/home/aemil/django-TOMIS-nptadwords'
site_name = 'TOMIS_nptadwords'


config = Config()
config['sudo']['password'] = '@e157Mil'
config['sudo']['user'] = 'aemil'
config['user'] = 'aemil'


@task
def deploy(c):
    with Connection(host='138.68.234.194', config=config, connect_kwargs={'password':'@e157Mil'}) as c:
        c.run('mkdir -p {}'.format(site_folder))
        with c.cd(site_folder):
            _get_latest_source(c)
            _update_virtualenv(c)
            _create_or_update_dotenv(c)
        with c.cd('{}/{}'.format(site_folder, site_name)):
            _update_static_files(c)
            _update_database(c)
        c.sudo('sudo systemctl restart gunicorn')


def _get_latest_source(c):
    if exists(c, '.git'):
        c.run('git fetch')
    else:
        c.run('git clone {} .'.fomat(REPO_URL))
    with c.cd('/Users/Nitrate/Documents/django-TOMIS-nptadwords'):
        current_commit = c.local("git log -n 1 --format=%H", env={'PATH': 'C:\\Program Files\\Git\\cmd'})
    c.run('git reset --hard {}'.format(current_commit.stdout))


def _update_virtualenv(c):
    if not c.run('pipenv --venv', warn=True):
        c.run('pipenv --three')
    #c.run('pipenv install --dev')


def _create_or_update_dotenv(c):
    append(c, '.env', 'DJANGO_DEBUG_FALSE=y')
    append(c, '.env', 'SITENAME={}'.format(site_name))
    current_contents = c.run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents.stdout:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append(c, '.env', 'DJANGO_SECRET_KEY={}'.format(new_secret))


def _update_static_files(c):
    c.run('pipenv run python manage.py collectstatic --noinput')


def _update_database(c):
    c.run('pipenv run python manage.py makemigrations --noinput')
    c.run('pipenv run python manage.py migrate --noinput')
