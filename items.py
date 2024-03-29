global node
config = node.metadata.get('grafana')

files = {
    "/etc/apt/sources.list.d/grafana.list": {
        'source': 'etc/apt/sources.list.d/grafana.list',
        'content_type': 'mako',
        'context': {},
        'tags': ['.pre'],
    },
    '/etc/grafana/grafana.ini': {
        'source': 'etc/grafana/grafana.ini.jinja2',
        'content_type': 'jinja2',
        'context': {
            'admin_username': config.get('admin_username'),
            'admin_password': config.get('admin_password'),
            'admin_email': config.get('admin_email'),
            'secret_key': config.get('secret_key'),
            'http': config.get('http'),
            'database': config.get('database'),
            'auth_github': config.get('auth').get('github'),
        },
        'owner': 'grafana',
        'group': 'grafana',
        'needs': {
            'pkg_apt:grafana',
        },
        'triggers': [
            'svc_systemd:grafana-server:restart',
        ],
    }
}

actions = {
    "import_grafana_key": {
        'command': 'curl https://apt.grafana.com/gpg.key | '
                   'gpg --dearmor > /etc/apt/trusted.gpg.d/grafana_signing.gpg',
        'unless': 'test -f /etc/apt/trusted.gpg.d/grafana_signing.gpg',
        'tags': [
            '.pre'
        ],
        'needs': [
            'file:/etc/apt/sources.list.d/grafana.list',
            'pkg_apt:gpg',
            'pkg_apt:curl',
        ],
        'triggers': [
            'action:force_update_apt_cache',
        ],
    },
}

pkg_apt = {
    'grafana': {
        'installed': True,
        'needs': [
            'file:/etc/apt/sources.list.d/grafana.list',
            'action:import_grafana_key',
            'action:force_update_apt_cache',
        ],
    }
}

svc_systemd = {
    "grafana-server": {
        'running': True,
        'enabled': True,
        'needs': [
            'file:/etc/grafana/grafana.ini',
            'pkg_apt:grafana'
        ],
    }
}
