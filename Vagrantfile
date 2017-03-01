# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "debian/contrib-jessie64"
  config.vm.network "private_network", ip: "10.0.0.110"

  config.ssh.paranoid = false
  config.ssh.forward_agent = true

  config.vm.provision "ansible" do |ansible|
    ansible.inventory_path = "ansible/inventories/development"
    ansible.playbook = "ansible/site.yml"
    ansible.limit = "all"
    ansible.ask_vault_pass = true
  end
end
