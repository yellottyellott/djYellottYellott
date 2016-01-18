from os.path import dirname, realpath, join, expanduser

from fabric.api import task, env
from fabric.api import local, run, sudo
from fabric.api import cd
from fabric.utils import abort
from fabric.contrib.console import confirm
from fabric.contrib.files import append, exists

import shortstack


PROJECT_ROOT = dirname(realpath(__file__))

env.forward_agent = True


@task
def vagrant():
    env.hosts = ['10.0.0.10']
    env.user = "vagrant"
    env.password = "vagrant"

    # Provisioning
    env.inventory = join(PROJECT_ROOT, "config/hosts/vagrant")
    env.playbook = join(PROJECT_ROOT, "config/site.yml")

    # Deployment
    env.branch = 'dev'
    env.settings_file = 'dev.py'
    env.requirements_file = 'dev.txt'

# Set vagrant as our default environment.
vagrant()


@task
def dev():
    env.hosts = ['dev.yellottyellott.com']
    env.user = "moose"
    env.password = None

    # Provisioning
    env.inventory = join(PROJECT_ROOT, "config/hosts/dev")
    env.playbook = join(PROJECT_ROOT, "config/site.yml")

    # Deployment
    env.branch = 'dev'
    env.settings_file = 'dev.py'
    env.requirements_file = 'dev.txt'

@task
def prod():
    """ Sets the target environment to production. """
    question = "You're trying to execute a command on PRODUCTION. \
        \nAre you sure you want to do this?"
    if not confirm(question=question, default=False):
        abort("Aborting.")

    env.hosts = ['yellottyellott.com']
    env.user = "moose"
    env.password = None

    # Provisioning
    env.inventory = join(PROJECT_ROOT, "config/hosts/prod")
    env.playbook = join(PROJECT_ROOT, "config/site.yml")

    # Deployment
    env.branch = 'master'
    env.settings_file = 'prod.py'
    env.requirements_file = 'prod.txt'


@task
def ssh_copy_id(key_file='~/.ssh/id_rsa.pub'):
    key_file = expanduser(key_file)

    if not key_file.endswith('pub'):
        raise RuntimeWarning('Trying to push non-public part of key pair')

    if not exists('~/.ssh'):
        run('mkdir -m 0700 ~/.ssh')

    with open(key_file) as f:
        key_text = f.read()
        append('~/.ssh/authorized_keys', key_text)
        run('chmod 0600 ~/.ssh/authorized_keys')


@task
def provision():
    ssh_copy_id()
    kwargs = dict(
        inventory=env.inventory,
        playbook=env.playbook,
        user=env.user,
    )
    local("ansible-playbook -i {inventory} {playbook} -u {user} -K".format(**kwargs))


@task
def deploy():
    project_root = '/home/%s/yellottyellott' % env.user
    app_root = join(project_root, 'webapp')
    virtualenv_root = join(project_root, 'venv')
    git_url = 'git@github.com:yellottyellott/djYellottYellott.git'
    git_branch = env.branch
    requirements_file = join(app_root, 'requirements/%s' % env.requirements_file)
    settings_file = join(app_root, 'project/settings/%s' % env.settings_file)

    shortstack.deploy(
        app_root=app_root,
        virtualenv_root=virtualenv_root,
        git_url=git_url,
        git_branch=git_branch,
        requirements_file=requirements_file,
        settings_file=settings_file
    )

    shortstack.recreate_db(virtualenv_root=virtualenv_root, app_root=app_root)
    shortstack.load_test_data(virtualenv_root=virtualenv_root, app_root=app_root)


@task
def runserver():
    local('vagrant up')
    with cd('/vagrant'):
        env.output_prefix = ''
        sudo('./manage.py runserver 0.0.0.0:8000')

