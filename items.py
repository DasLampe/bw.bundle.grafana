import os

global node

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
            'http': node.metadata.get('grafana').get('http'),
            'database': node.metadata.get('grafana').get('database'),
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
            'file:/etc/apt/sources.list.d/grafana.list'
        ],
        'triggers': [
            'action:force_update_apt_cache',
        ],
    },
    'reset_grafana_admin_password': {
        'command': f'grafana-cli admin reset-admin-password {node.metadata.get("grafana").get("admin_password")}',
        'needs': [
            'svc_systemd:grafana-server',
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
