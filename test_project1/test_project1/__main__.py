"""
For more information on this file, see
https://docs.cotletteproject.com/en/dev/howto/deployment/asgi/
"""

import os
import uvicorn

from .settings import DEBUG, settings


num_cores = os.cpu_count()

uvicorn.run(
    'app.app:app',
    host=settings.server_host,
    port=settings.server_port,
    reload=True if DEBUG else False,
    workers=1 if DEBUG else num_cores + 1,
)