#!/usr/bin/env python3
from chibi.config import basic_config
from chibi.command import yum, systemctl, command, firewall, rpm
from chibi.command.echo import cowsay
from chibi.file import Chibi_file, Chibi_path
from chibi.file.snippets import inflate_dir
from chibi.net import download


basic_config()
file_check_path = Chibi_path( '~/provision_installed' )
file_check = Chibi_file( file_check_path )


version_to_check = "rabbitmq\n".format( file=__file__, )


if __name__ == "__main__" and not version_to_check in file_check:
    cowsay( "instalando rabbitmq" )
    rpm.rpm_import( 'https://artifacts.elastic.co/GPG-KEY-elasticsearch' )
    download(
        "https://www.rabbitmq.com/releases/rabbitmq-server/v3.6.1/"
        "rabbitmq-server-3.6.1-1.noarch.rpm",
        directory='/tmp', file_name='rabbitmq.rpm' )

    yum.local_install( "/tmp/rabbitmq.rpm" )

    systemctl.enable( 'firewalld' )
    systemctl.start( 'firewalld' )

    ports = [ "8883", "61613-61614", "15672", "5671-5672", "25672", "4369" ]
    for port in ports:
        firewall.add_port( ports=port )
    firewall.reload()

    command( 'setsebool', "-P", "nis_enabled", "1" )
    systemctl.enable( 'rabbitmq-server' )
    systemctl.start( 'rabbitmq-server' )

    file_check.append( version_to_check )

    cowsay( "termino de instalar rabbitmq" )