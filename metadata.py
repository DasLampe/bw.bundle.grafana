global repo
global node

defaults = {
    'grafana': {
        'admin_password': repo.vault.password_for("grafana_admin_{}".format(node.name)),
        'create_database': True,
        'database':  {
            'host': '127.0.0.1',
            'port': '5432',
            'name': 'grafana',
            'user': 'grafana',
            'password': repo.vault.password_for("postgres_user_{}_{}".format('grafana', node.name)),
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
            },
        },
    },
}

@metadata_reactor
def add_postgresql_integration(metadata):
    if not node.has_bundle("postgres"):
        raise DoNotRunAgain

    if metadata.get('prometheus').get('create_database'):
        return {
            'postgres': {
                'databases': {
                    metadata.get('prometheus').get('database').get('name'): {
                        'owner_name': metadata.get('prometheus').get('database').get('user'),
                        'owner_password': metadata.get('prometheus').get('database').get('password'),
                    },
                },
            }
        }

    return {}