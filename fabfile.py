import random
import os
from fabric import Connection
from patchwork.files import exists, append
from invoke import task


REPO_URL = 'https://github.com/mrnitrate/TOMIS_nptadwords'
site_folder = '/home/aemil/django-TOMIS-nptadwords'
site_name = 'TOMIS_nptadwords'


@task
def deploy(c):
    with Connection(host='138.68.234.194',user='aemil', port='22', connect_kwargs={'password':'@e157Mil'}) as c:
        c.run(f'mkdir -p {site_folder}')
        with c.cd(site_folder):
            print('1')
            _get_latest_source(c)
            print('2')
            _update_virtualenv(c)
            print('3')
            _create_or_update_dotenv(c)

            with c.cd(f'{site_folder}/{site_name}'):
                print('4')
                _update_static_files(c)
                print('5')
                _update_database(c)
                print('6')


def _get_latest_source(c):
    if exists(c, '.git'):
        c.run('git fetch')
    else:
        c.run(f'git clone {REPO_URL} .')
    with c.cd('/Users/Nitrate/Documents/django-TOMIS-nptadwords'):
        current_commit = c.local("git log -n 1 --format=%H", env={'PATH': 'C:\\Program Files\\Git\\cmd'})
    c.run(f'git reset {current_commit.stdout}')


def _update_virtualenv(c):
    if not c.run('pipenv --venv',warn=True):
        c.run('pipenv --three')
    c.run('pipenv install --dev')


def _create_or_update_dotenv(c):
    append(c,'.env', 'DJANGO_DEBUG_FALSE=y')
    append(c,'.env', f'SITENAME={site_name}')
    current_contents = c.run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents.stdout:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append(c,'.env', f'DJANGO_SECRET_KEY={new_secret}')


def _update_static_files(c):
    c.run('pipenv run python manage.py collectstatic --noinput')


def _update_database(c):
    c.run('pipenv run python manage.py migrate --noinput')
