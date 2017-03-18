CONFIG = {
    'mode': 'wsgi',
    'working_dir': '/home/box/web/ask',
    'python': '/usr/bin/python3',
    'args': (
        '--bind=0.0.0.0:8000',
        '--daemon',
        '--workers=2',
        '--timeout=60',
        '--log-level=debug'
        'ask.wsgi:application',
    ),
}
