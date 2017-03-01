"""Provision and deploy.

Usage:
    fab ENVIRONMENT TASK

    $ fab development provision
    $ fab development ping
    $ fab development deploy
"""
import re

from fabric.api import task, env, local, run
from fabric.contrib.console import confirm
from fabric.utils import puts, abort
from fabric.operations import put
from fabric.context_managers import cd, shell_env


env.user = 'yellottyellott'
env.use_ssh_config = True
env.inventory = ''
env.playbook = 'ansible/site.yml'


@task
def development():
    """Use development settings."""
    env.name = 'development'
    env.hosts = ['dev.yellottyellott.com']
    env.inventory = 'ansible/inventories/development'


@task
def staging():
    """Use staging settings."""
    env.name = "staging"
    env.hosts = ['staging.yellottyellott.com']
    env.inventory = 'ansible/inventories/staging'


@task
def production():
    """Use production settings."""
    prompt = ("You are trying to execute a command on PRODUCTION.\n"
              "Are you sure you want to do this?")
    if not confirm(question=prompt, default=False):
        abort("Cancelled by user.")

    env.name = "production"
    env.hosts = ['yellottyellott.com']
    env.inventory = 'ansible/inventories/production'


@task
def ping():
    """Ping host."""
    cmd = "ansible --inventory-file {} --one-line all -m ping"
    cmd = cmd.format(env.inventory)
    with shell_env(ANSIBLE_CONFIG='ansible/ansible.cfg'):
        local(cmd)


@task
def provision():
    """Provision host with ansible-playbook."""
    cmd = "ansible-playbook --inventory-file {} --ask-become-pass --ask-vault-pass {}"
    cmd = cmd.format(env.inventory, env.playbook)
    with shell_env(ANSIBLE_CONFIG='ansible/ansible.cfg'):
        local(cmd)


@task
def build(treeish="head"):
    """Build a release."""
    version = local("git describe {}".format(treeish), capture=True)

    is_pushed = local("git branch -r --contains {}".format(version), capture=True)
    if not is_pushed:
        abort("Commit not pushed to remote repository.")

    output = "/tmp/{}.tar.gz".format(version)
    prefix = "{}/".format(version)
    cmd = "git archive --prefix={prefix} --format=tar.gz --output={output} {version}:src"
    local(cmd.format(prefix=prefix, output=output, version=version))
    puts("\nBuilt: {} at: {}".format(version, output))
    return output


@task
def deploy(treeish="head"):
    """Build and deploy a release."""
    local_path = build(treeish)
    tarball_name = local_path.split('/').pop()
    version = re.sub('\.tar\.gz$', '', tarball_name)
    releases_dir = '/srv/yellottyellott/releases'
    remote_path = '{}/{}'.format(releases_dir, tarball_name)
    put(local_path, remote_path)
    with cd(releases_dir):
        run('tar -xzf {}'.format(tarball_name))
        run('rm -f {}'.format(tarball_name))
        run('ln -sfn {} current'.format(version))
