#
# A fabric deploy script for a django project using uwsgi + nginx (is debian/ubuntu focused)
#
# The nginx virtual host conf and uwsgi.ini should reside in the project root:
#     - virtual host conf filename should be: PROJECT_NAME_nginx.conf
#     - uwsgi conf filename should be: uwsgi.ini
#
# The deployment is mercurial based, but the script requires little changes for using git
# deployment works as follow:
#     $ fab (devel|staging|production) install_system_deps #only once
#     $ fab (devel|staging|production) deploy[:branch_name]
#
# rollback:
#     $ fab (devel|staging|production) rollback
#

import time
import os.path

from fabric.api import *
from fabric.contrib import project


PROJECT_NAME = "django-TOMIS-nptadwords"

# Remote location deploy dir
SITE_ROOT = "/home/aemil/%s" % PROJECT_NAME
# Sub directories to be created inside SITE_ROOT
SUB_DIRS = {
    'RELEASES': 'releases',
    'VENV': 'venv',
    'CONF': 'conf',
    'LOG': 'log',
    'STATIC': 'static'
}

# The place where all the code revisions will live
CODE_DIR = os.path.join(SITE_ROOT, SUB_DIRS['RELEASES'])
# Symbolic link name for the current release
CURRENT_RELEASE = "current"
# Remote config dir
CONF_DIR = os.path.join(SITE_ROOT, SUB_DIRS['CONF'])
# Python Virtual Environment for the project
VENV_DIR = os.path.join(SITE_ROOT, SUB_DIRS['VENV'])
# Temp folder
TMP_DIR = "/tmp"

# Max number of items kept in releases folder
RELEASES_HISTORY = 5


def _create_dirs(site_root, sub_dirs):
    """
    Creates the remote directory structure for deploying the project
    """
    with settings(warn_only=True):
        sudo("mkdir %s" % site_root)
        with cd(site_root):
            for key, dir in sub_dirs.items():
                sudo("mkdir %s" % dir)
        _fix_perms(site_root)


def _check_folders(site_root, sub_dirs):
    """
    Checks the existence of all needed folders
    """
    with settings(warn_only=True):
        if run("test -d %s" % site_root).failed:
            return False
        status = True
        with cd(site_root):
            for key, dir in sub_dirs.items():
                status &= not run("test -d %s" % dir).failed

        return status


def _fix_perms(site_root):
    """
    Updates the folder permissions
    """
    sudo("chown -R %s:%s %s" % (env.user, "www-data", site_root))
    sudo("chmod -R g+rw %s" % site_root)


def _create_virtual_env(venv_dir):
    """
    Creates the virtual environment for the project
    """
    #run("virtualenv --system-site-packages %s" % venv_dir)
    run("virtualenv %s" % venv_dir)


def devel():
    """
    Sets the environment variables to deploy to localhost
    """
    env.hosts = ['localhost']


def staging():
    """
    Sets the environment variables to deploy to staging environment
    """
    env.hosts = ['staging-host1']
    env.user = 'staging-user'


def production():
    """
    Sets the environment variables to deploy to production environment
    """
    env.hosts = ['138.68.234.194']
    env.user = 'aemil'


def _update_project(code_dir, branch, release_date):
    """
    Updates the project code in the remote host(s)
    """
    local("git pull origin master")
    destination_dir = os.path.join(code_dir, release_date)
    run("mkdir %s" % destination_dir)
    with cd(code_dir):
        exclude_pattern = ['.hg/', '.gitignore', '.idea/', '*.pyc']
        project.rsync_project(remote_dir=destination_dir, exclude=exclude_pattern)

    _create_code_symlink(code_dir, destination_dir)


def _install_requirements(venv_dir, code_dir, release_date, project_name):
    """
    Install the requirements for the project as listed in requirements.txt file
    """
    requirements = os.path.join(code_dir, release_date, project_name, "requirements.txt")
    with cd(venv_dir):
        run("source bin/activate && pip install -r %s" % requirements)


def _create_code_symlink(code_dir, target):
    """
    Creates symbolic link in the releases folder
    """
    link_path = os.path.join(code_dir, CURRENT_RELEASE)
    with cd(code_dir):
        with settings(warn_only=True):
            run("unlink %s" % link_path)
            run("ln -s %s %s" % (target, link_path))


def _get_releases_list(code_dir):
    """
    Returns a list of all releases directories, ignoring the symbolic link
    to the 'current' release
    """
    dirs = run("ls -r -1 %s" % code_dir)
    from contextlib import nested   # For executing nested contexts in python 2.5 and 2.6, deprecated for 2.7

    with nested(settings(warn_only=True), hide('warnings', 'running', 'stdout', 'stderr')):
        with cd(code_dir):
            # All directories but the 'current' symbolic link
            releases = [os.path.join(code_dir, item) for item in dirs.splitlines() if run("test -L %s" % item).failed]

    return releases


def _clean_history(code_dir, max_history):
    """
    Deletes the oldest version of code deployed in releases folder
    """
    releases = _get_releases_list(code_dir)
    if len(releases) <= max_history:
        return

    print "Cleaning oldest releases:"
    [run("rm -rf %s" % item) for item in releases[max_history:]]


def _link_uwsgi_conf(conf_dir, code_dir, uwsgi_ini_file):
    """
    uWSGI configuration
    """

    conf_destination = os.path.join(conf_dir, uwsgi_ini_file)
    conf_source = os.path.join(code_dir, CURRENT_RELEASE, PROJECT_NAME, uwsgi_ini_file)

    with settings(warn_only=True):
        run("unlink %s" % conf_destination)
        run("ln -s %s %s" % (conf_source, conf_destination))


def _restart_uwsgi(conf_dir, uwsgi_ini_file):
    """
    Restart the uWSGI container
    """
    pid_file_name = PROJECT_NAME + "_uwsgi.pid"
    pid_full_path = os.path.join(SITE_ROOT, pid_file_name)

    with settings(warn_only=True):
        conf_destination = os.path.join(conf_dir, uwsgi_ini_file)
        if run("test -f %s" % pid_full_path).failed:
            run("uwsgi --ini %s" % conf_destination)
        else:
            run("uwsgi --touch-reload %s" % conf_destination)


def _link_nginx_conf(code_dir, vhost_file):
    """
    Nginx configuration
    """
    sites_available = "/etc/nginx/sites-available"
    sites_enabled = "/etc/nginx/sites-enabled"

    conf_source = os.path.join(code_dir, CURRENT_RELEASE, PROJECT_NAME, vhost_file)
    with settings(warn_only=True):
        sudo("cp %s %s" % (conf_source, sites_available))
        sudo("ln -f -s %s %s" % (os.path.join(sites_available, vhost_file), os.path.join(sites_enabled, vhost_file)))


def _restart_nginx():
    """
    Simply restart the nginx service
    """
    sudo("service nginx restart")


def _collect_static_files(venv_dir, code_dir, project_name):
    """
    Collect all the static files into the final destination that will be served directly by the web server
    """
    project_root = os.path.join(code_dir, CURRENT_RELEASE, project_name)
    with cd(project_root):
        activate_venv = os.path.join(venv_dir, "bin", "activate")
        with prefix("source %s" % activate_venv):
            run("python manage.py collectstatic --noinput")


def install_system_deps():
    """
    Install the S.O needed packages (debian focus) and install 'virtualenv' and 'uwsgi' as global python packages
    """
    sudo("apt-get install -y python-dev python-pip libgmp-dev libxml2-dev libxslt1-dev nginx")
    sudo("pip install virtualenv")
    sudo("pip install uwsgi")


def deploy(branch='default'):
    """
    deploy[:branch], deploys the code (in the specified branch or default) and installs the dependencies
    """
    if not _check_folders(SITE_ROOT, SUB_DIRS):
        _create_dirs(SITE_ROOT, SUB_DIRS)

    release_date = time.strftime("%Y%m%d%H%M%S")
    uwsgi_ini_file = "uwsgi.ini"
    vhost_file = "%s_nginx.conf" % PROJECT_NAME

    _update_project(CODE_DIR, branch, release_date)
    _create_virtual_env(VENV_DIR)
    _fix_perms(SITE_ROOT)

    _install_requirements(VENV_DIR, CODE_DIR, release_date, PROJECT_NAME)
    _collect_static_files(VENV_DIR, CODE_DIR, PROJECT_NAME)

    _link_uwsgi_conf(CONF_DIR, CODE_DIR, uwsgi_ini_file)
    _restart_uwsgi(CONF_DIR, uwsgi_ini_file)
    _link_nginx_conf(CODE_DIR, vhost_file)
    _restart_nginx()

    _clean_history(CODE_DIR, RELEASES_HISTORY)


def rollback():
    """
    Rollbacks the code to the previous release if exists
    """
    releases = _get_releases_list(CODE_DIR)

    if len(releases) < 2:
        print "Cannot rollback because number of releases is: %s" % len(releases)
        return

    _create_code_symlink(CODE_DIR, releases[1])
    run("rm -rf %s" % releases[0])
    _fix_perms(SITE_ROOT)
    _restart_uwsgi()
    _restart_nginx()
