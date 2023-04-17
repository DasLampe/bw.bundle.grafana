global repo, node, metadata_reactor, DoNotRunAgain

defaults = {
    'grafana': {
        'admin_username': 'admin',
        'admin_password': repo.vault.password_for("grafana_admin_{}".format(node.name)),
        'admin_email': 'admin@localhost',
        'secret_key': repo.vault.password_for(f'grafana_secret_key_{node.name}'),
        'create_database': True,
        'database':  {
            'host': '127.0.0.1',
            'port': '5432',
            'name': 'grafana',
            'user': 'grafana',
            'password': repo.vault.password_for("postgres_user_{}_{}".format('grafana', node.name)),
        },
        'http': {
            'domain': 'localhost',
            'root_url': '%(protocol)s://%(domain)s:%(http_port)s/',
            'addr': '127.0.0.1',
            'port': '3000',
        },
        'auth': {
            'github': {
                'enabled': False,
                'allow_sign_up': True,
                'auto_login': False,
                'client_id': '',
                'client_secret': '',
                'scopes': ['user:email', 'read:org'],
                'auth_url': 'https://github.com/login/oauth/authorize',
                'token_url': 'https://github.com/login/oauth/access_token',
                'api_url': 'https://api.github.com/user',
                'allowed_domains': [],
                'team_ids': [],
                'allowed_organizations': [],
                'role_attribute_path': '',
                'role_attribute_strict': False,
                'allow_assign_grafana_admin': False,
            }
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

    if metadata.get('grafana').get('create_database'):
        return {
            'postgres': {
                'databases': {
                    metadata.get('grafana').get('database').get('name'): {
                        'owner_name': metadata.get('grafana').get('database').get('user'),
                        'owner_password': metadata.get('grafana').get('database').get('password'),
                    },
                },
            }
        }

    return {}