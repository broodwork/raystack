"""
ASGI config for test_project1 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.cotletteproject.com/en/dev/howto/deployment/asgi/
"""

import os

from cotlette.core.asgi import get_asgi_application

os.environ.setdefault('COTLETTE_SETTINGS_MODULE', 'settings')

application = get_asgi_application()
