import contextlib

from fabric.api import env, task, local, abort, lcd
from fabric.api import settings, hide
from fabric.contrib.console import confirm

from .context_managers import mktemp
import ansible


@contextlib.contextmanager
def account_file():
    """Create temporary account.json file."""
    path = 'terraform/account.json'
    with mktemp(path, remove=False):
        with ansible.vault_file(), lcd('ansible'):
            decrypted = '../terraform/account.json'
            encrypted = '../terraform/account.json.aes'
            cmd = 'ansible-vault decrypt --output={} {}'.format(decrypted, encrypted)
            local(cmd)

        yield


def apply(path):
    """
    Create infra with terraform.

    0 - Succeeded, diff is empty (no changes)
    1 - Errored
    2 - Succeeded, there is a diff
    """
    with lcd(path), settings(hide('warnings'), warn_only=True):
        local("terraform init")
        result = local("terraform plan --refresh=true --detailed-exitcode")

    if result.return_code == 0:
        return

    if result.return_code == 1:
        abort("Terraform error.")

    if not confirm("Unapplied terraform changes. Apply now?"):
        abort("Canceled.")

    with lcd(path):
        local("terraform apply --refresh=true")


@task
def terraform():
    """Create infra with terraform."""
    with account_file():
        apply('terraform/common')
        apply('terraform/{}'.format(env.name))
