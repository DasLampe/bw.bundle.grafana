default_password_postgres = repo.vault.password_for("postgres_user_{}_{}".format('grafana', node.name))

defaults = {
    'grafana': {
        'admin_password': repo.vault.password_for("grafana_admin_{}".format(node.name)),
        'database':  {
            'name': 'grafana',
            'user': 'grafana',
            'password': default_password_postgres,
        },
        'http': {
            'addr': '127.0.0.1',
            'port': '3000',
        },
    },
    'apt': {
        'packages':  {
            'apt-transport-https': {
                'installed': True,
            },
            'software-properties-common': {
                'installed': True,
            }
        }
    },
    'postgres': {
        'databases': {
            'grafana': {
                'owner_name': 'grafana',
                'owner_password': default_password_postgres,
            },
        },
    },
}
