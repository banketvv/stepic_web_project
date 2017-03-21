CONFIG = {
    'mode': 'wsgi',
    'working_dir': '/home/box/web/ask/ask',
    'python': '/usr/bin/python',
    'args': (
        '--bind=0.0.0.0:8000',
        '--workers=2',
        '--timeout=60',
        '--log-level=debug',
        '--log-file=/home/box/gunicorn.log',
        'wsgi',
    ),
}
