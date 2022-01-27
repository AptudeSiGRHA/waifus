from .base import Centos_7


class Nginx( Centos_7 ):
    scripts = (
        "nginx/install.py",
        "nginx/provision.py",
        ( "nginx/enable.py", 'enable', 'waifus', 'kibana' ),
        ( "nginx/enable.py", 'enable', 'default' ),

        ( "systemd/systemd.py", 'enable', 'nginx.service' ),
        ( "systemd/systemd.py", 'restart', 'nginx.service' ),

        "elasticsearch/beat/filebeat_install.py",
        "elasticsearch/beat/filebeat_nginx.py",
        ( "systemd/systemd.py", 'start', 'filebeat.service' )
    )


class Ikaros( Nginx ):
    extra_hosts = (
        'kibana', 'waifus', 'sigrha.com.mx',
        'api.sigrha.client.aptude.com',
        'api.sigrha.opportunities.aptude.com',
        'api.sandbox.client.sigrha.com',
        'api.sandbox.opportunities.sigrha.com',
        'api.sandbox.sigrha.com',
        'sandbox.sigrha.com',
    )


class Astraea( Nginx ):
    pass


class Caos( Nginx ):
    pass


class Nymph( Nginx ):
    pass
