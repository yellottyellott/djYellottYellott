import contextlib
import getpass
import os

from fabric.api import env, task, local, lcd

from .context_managers import mktemp


@contextlib.contextmanager
def vault_file():
    """Create temporary vault password file."""
    path = 'ansible/vault-password.txt'
    if os.path.isfile(path):
        yield
    else:
        pw = getpass.getpass("Vault password: ")
        with mktemp(path, remove=False) as f:
            f.write(pw)
            f.flush()
            yield


@task
def ansible():
    """Provision host with ansible-playbook."""
    with vault_file(), lcd('ansible'):
        cmd = "ansible-playbook --inventory-file {} site.yml"
        cmd = cmd.format(env.inventory)
        local(cmd)
