# -*- mode: ruby -*-
# vi: set ft=ruby :
#
require 'yaml'

REL_DIR = File.dirname(__FILE__)
HOST_SHARE_FOLDER = REL_DIR + "/" + "src"
HOST_BACKUPS_SHARE_FOLDER = REL_DIR + "/" + "backups"
GUEST_SHARE_FOLDER = "/home/vagrant/src"
GUEST_SHARE_FOLDER_PROVISION = "/home/vagrant/provision"

BACKUPS_SHARE_FOLDER = "/home/vagrant/backups"


Vagrant.configure(2) do |config|

	#config.vm.box = "box-cutter/centos70"
	#config.vm.box = "insaneworks/centos"
	config.vm.box = "geerlingguy/centos7"

	start_ip = "192.168.2.150"

	natural_host = File.open( REL_DIR + "/" + "provision/natural_hosts", "r")
	hosts = natural_host.read

	machines = YAML.load_file( REL_DIR + "/" +  'machines.yml' )


	config.vm.synced_folder HOST_BACKUPS_SHARE_FOLDER, BACKUPS_SHARE_FOLDER, owner: "vagrant", group: "vagrant", create: true
	config.vm.synced_folder HOST_SHARE_FOLDER, GUEST_SHARE_FOLDER, owner: "vagrant", group: "vagrant", create: true
	config.vm.synced_folder 'provision', GUEST_SHARE_FOLDER_PROVISION, owner: "vagrant", group: "vagrant", create: true

	# nginx and django
	split_ip = start_ip.split( '.' )

	aux_machines = {}
	for k, v in machines
		machines_names = v[ 'machines' ]
		machines_config = v[ 'config' ]

		hosts << "\# machines #{ k }\n"

		machines_names.each { |name|
			aux_machines[ name ] = machines_config
			current_ip = split_ip.join( '.' )
			config.vm.define name, primary: true do |m|
				machines_config = aux_machines[ name ]
				m.vm.host_name = name
				m.vm.network "public_network", bridge: "wlp2s0", ip: current_ip
				m.vm.provider "virtualbox" do |vb|
					vb.name = name
					vb.memory = machines_config[ 'ram' ]
					vb.cpus = machines_config[ 'cpus' ]
				end
				machines_config[ 'provisions' ].each { |provision|
					args = provision.fetch( 'args', '' ).sub '{name}', name
					path = REL_DIR + "/" + provision[ 'path' ]
					if ( args )
						m.vm.provision :shell, path: path, args: args
					else
						m.vm.provision :shell, path: path
					end
				}
			end
			extra_host = v.fetch( 'extra_hosts', [] )
			hosts << "#{ current_ip }\t\t#{ name } #{ extra_host.join( ' ' ) }\n"
			split_ip[3] = split_ip[3].to_i + 1
		}
	end

	hosts_end = File.open( REL_DIR + "/" + "provision/hosts", "w")
	hosts_end.write( hosts )
	hosts_end.close()

end
