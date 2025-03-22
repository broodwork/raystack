"""
WSGI config for test_project1 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.cotletteproject.com/en/dev/howto/deployment/wsgi/
"""

import os

from cotlette.core.wsgi import get_wsgi_application

os.environ.setdefault('COTLETTE_SETTINGS_MODULE', 'test_project1.settings')

application = get_wsgi_application()
