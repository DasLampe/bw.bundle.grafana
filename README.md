# Bundlewrap for Grafana
Install and configure Grafana via Bundlewrap.

# Dependencies
- [Postgres Bundle](https://github.com/sHorst/bw.bundle.postgres)
- [Debian Bundle](https://github.com/sHorst/bw.bundle.debian)

# Config
See `defaults` in `metadata.py`.

```python
metadata = {
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
```