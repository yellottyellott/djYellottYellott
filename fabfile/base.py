"""Provision and deploy.

Usage:
    fab ENVIRONMENT TASK

    $ fab development provision deploy
    $ fab development deploy
"""
import re

from fabric.api import env, task, local, run, puts, abort, cd, put, settings, hide
from fabric.contrib.console import confirm

from . import terraform, ansible


env.user = 'yellottyellott'
env.use_ssh_config = True


@task(alias='dev', default=True)
def dev():
    """Use development settings."""
    env.name = 'dev'
    env.hosts = ['dev.yellottyellott.com']
    env.inventory = 'inventories/dev'


@task()
def stage():
    """Use stage settings."""
    env.name = "stage"
    env.hosts = ['stage.yellottyellott.com']
    env.inventory = 'inventories/stage'


@task()
def prod():
    """Use prod settings."""
    prompt = ("You are trying to execute a command on PRODUCTION.\n"
              "Are you sure you want to do this?")
    if not confirm(question=prompt, default=False):
        abort("Canceled.")

    env.name = "prod"
    env.hosts = ['yellottyellott.com']
    env.inventory = 'inventories/prod'


@task
def provision(default=True):
    """Create and provision infra."""
    with ansible.vault_file():
        terraform.terraform()
        ansible.ansible()


@task
def build(treeish='head'):
    """Build a release."""
    version = local("git describe {}".format(treeish), capture=True)

    with settings(hide('warnings'), warn_only=True):
        cmd = "git diff-index --quiet {} --".format(treeish)
        is_committed = local(cmd).succeeded
        cmd = "git branch -r --contains {}".format(version)
        is_pushed = local(cmd, capture=True)

    if not is_committed:
        prompt = "Uncommitted changes. Continue?"
        if not confirm(prompt, default=False):
            abort("Canceled.")

    if not is_pushed:
        prompt = "Commit not pushed. Continue?"
        if not confirm(question=prompt, default=False):
            abort("Canceled.")

    output = "/tmp/{}.tar.gz".format(version)
    prefix = "{}/".format(version)
    cmd = "git archive --prefix={prefix} --format=tar.gz --output={output} {version}:src"
    local(cmd.format(prefix=prefix, output=output, version=version))
    puts("\nBuilt: {} at: {}".format(version, output))
    return output


@task
def deploy(treeish='head'):
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
